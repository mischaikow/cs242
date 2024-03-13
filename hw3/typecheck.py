from src.lam import *
from typing import List


def typecheck(prog: Prog) -> List[Type]:
    ## my counters
    a = []
    b = []

    def gen_constr(A, e):
        if isinstance(e, Var):
            return TpVar(e.s)
        elif isinstance(e, Lam):
            pass
        elif isinstance(e, App):
            pass
        elif isinstance(e, IntConst):
            return IntTp()
        raise TypecheckingError("poorly constructed expression")

    def saturate_constr(A: set[tuple[Type, Type]]):
        old_size = -1
        while len(A) - old_size > 0:
            old_size = len(A)
            for left, right in A:
                A.add((right, left))

                for left_other, right_other in A:
                    if left == left_other:
                        A.add((right, right_other))
                        A.add((right_other, right))

                if isinstance(left, Func) and isinstance(right, Func):
                    A.add((left.a, right.a))
                    A.add((right.a, left.a))
                    A.add((left.b, right.b))
                    A.add((right.b, left.b))

    for defn in prog.defns:
        A = []
        constraints = gen_constr(A, defn.e)

    print(prog.defns[0])
    print(prog.defns[0].s)
    print(prog.defns[0].e)
    print(isinstance(prog.defns[0].e, Lam))
    print(prog.defns[0].e == Func)
    print(prog.defns[0].e == TpVar)
    # If there are no type errors, return a list of Types
    # Otherwise, throw TypecheckingError("msg")
    raise TypecheckingError("not implemented")
