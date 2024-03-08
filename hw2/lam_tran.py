import src.lam as lam
import src.ski as ski
import ski_eval

##########
# PART 3 #
##########
# T.S(.K():.I()mplement the below function `tran`.
# You can define helper functions outside `tran` and use them inside `tran`.


def tran(e: lam.Expr) -> ski.Expr:
    # BEGIN_YOUR_CODE

    def tran_ski(var: ski.Var, e: ski.Expr) -> ski.Expr:
        if isinstance(e, ski.S):
            return ski.App(ski.K(), ski.S())
        elif isinstance(e, ski.K):
            return ski.App(ski.K(), ski.K())
        elif isinstance(e, ski.I):
            return ski.App(ski.K(), ski.I())
        elif isinstance(e, ski.Var):
            if var.s == e.s:
                return ski.I()
            else:
                return ski.App(ski.K(), e)
        elif isinstance(e, ski.App):
            return ski.App(
                ski.App(ski.S(), tran_ski(var, e.e1)),
                tran_ski(var, e.e2),
            )

    if isinstance(e, lam.Var):
        return ski.Var(e.s)
    elif isinstance(e, lam.Lam):
        return tran_ski(ski.Var(e.s), tran(e.e))
    elif isinstance(e, lam.App):
        return ski.App(tran(e.e1), tran(e.e2))

    return e
    # END_YOUR_CODE
