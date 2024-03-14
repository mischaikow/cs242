from src.lam import *
from typing import Set, Tuple, List, Dict


def typecheck(prog: Prog) -> List[Type]:
    counter = [-1]
    S = set() 
    A: Dict[str, Type] = dict()

    def gen_constr(A: Dict[str, Type], e: Expr):
        match e:
            case Var() if e.s in CONSTS:
                return CONSTS[e.s]
            case Var() if e.s in A:
                return A[e.s]
            case Var():
                raise TypecheckingError(f'Variable needs definition: {e.s}')
            case Lam():
                counter[0] += 1
                alpha = TpVar(f'a{counter[0]}')
                return Func(alpha, gen_constr({**A, e.s: alpha}, e.e))
            case App():
                counter[0] += 1
                beta = TpVar(f'a{counter[0]}')
                dummy = (gen_constr(A, e.e1), Func(gen_constr(A, e.e2), beta))
                print('-- new constraint --')
                print(e)
                print(dummy)
                S.add(dummy)
                return beta
            case IntConst():
                return IntTp()
            case _:
                raise TypecheckingError("poorly constructed expression")

    def saturate_constr(S: Set[Tuple[Type, Type]]):
        old_size = -1
        while len(S) - old_size > 0:
            old_size = len(S)
            for left, right in S.copy():
                S.add((right, left))

                for left_other, right_other in S.copy():
                    if left == left_other:
                        S.add((right, right_other))
                        S.add((right_other, right))

                if isinstance(left, Func) and isinstance(right, Func):
                    S.add((left.a, right.a))
                    S.add((right.a, left.a))
                    S.add((left.b, right.b))
                    S.add((right.b, left.b))

    def typechecking(A: Dict[str, Type], S: Set[Tuple[Type, Type]]):
        global X
        X = set()

        for left, right in S:
            if isinstance(left, Func) and isinstance(right, IntTp):
                raise TypecheckingError("forbidden equality between int and function type")

        def canonicalizer(S: Set[Tuple[Type, Type]], tau: Type):

            def constraintFinder(S, alpha):
                alpha_set = set()
                alpha_set.add(alpha)

                for left, right in S:
                    if left == alpha:
                        alpha_set.add(right)
                        if not isinstance(right, TpVar):
                            return True, right
                
                if len(alpha_set) > 1:
                    return True, min(alpha_set, key=lambda t: t.s)
                
                return False, -1

            try:
                if tau in X:
                    raise TypecheckingError('Hit a canonicalization loop - infinite types')
                X.add(tau)

                match tau:
                    case IntTp():
                        return tau
                    case Func():
                        return Func(canonicalizer(S, tau.a), canonicalizer(S, tau.b))
                    case TpVar():
                        isC, right = constraintFinder(S, tau)

                        if isC:
                            return canonicalizer(S, right)
                        else:
                            return tau

            except (TypecheckingError) as e:
                X.add(tau)
                raise e

            finally:
                X.remove(tau)

        for a_type in A:
            A[a_type] = canonicalizer(S, A[a_type])


    for defn in prog.defns:
        A[defn.s] = gen_constr(A, defn.e)
    print(S)
    print(A)
    saturate_constr(S)
    typechecking(A, S)

    # If there are no type errors, return a list of Types
    return list(A.values())
    # Otherwise, throw TypecheckingError("msg")
    raise TypecheckingError("not implemented")
