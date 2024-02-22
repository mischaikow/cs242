import src.ski as ski

##########
# PART 1 #
##########
# TASK: Implement the below function `eval`.
    
def eval(e: ski.Expr) -> ski.Expr:
    def eval_helper(e: ski.Expr):
        if (isinstance(e, ski.App) and isinstance(e.e1, ski.App) and
                isinstance(e.e1.e1, ski.App) and isinstance(e.e1.e1.e1, ski.S)):
            return eval(ski.App(ski.App(e.e1.e1.e2, e.e2), ski.App(e.e1.e2, e.e2))), False

        if (isinstance(e, ski.App) and isinstance(e.e1, ski.App) and
                isinstance(e.e1.e1, ski.K)):
            return eval(e.e1.e2), False

        if (isinstance(e, ski.App) and isinstance(e.e1, ski.I)):
            return eval(e.e2), False
        
        if (isinstance(e, ski.App)):
            left, is_l_done = eval_helper(e.e1)
            right, is_r_done = eval_helper(e.e2)
            ## Every day we stray further from lecture 3, page 24
            ## right, is_r_done = e.e2, True

            return ski.App(left, right), is_l_done and is_r_done

        return e, True
    
    e, done = eval_helper(e)
    while not done:
        e, done = eval_helper(e)

    # BEGIN_YOUR_CODE
    return e
    # END_YOUR_CODE
