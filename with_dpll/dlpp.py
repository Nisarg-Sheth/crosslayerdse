import random

random.seed(111)

def dpll_solver(decision_strat,constraints,literal):
    for con in constraints:
        if not bool(con[0]) and con[1]==0 and con[2]=='=':
            constraints.remove(con)
        if not bool(con[0]) and con[1]>=0 and con[2]=='<=':
            constraints.remove(con)
        elif not bool(con[0]):
            return false, None
    assignment={}
    if len(constraints) == 0:
        return True, assignment

    cur_var = decision_strat[literal][0]
    var_val = decision_strat[literal][2]

    new_cons = [con for con in constraints]
    for con in new_cons:
        if cur_val in con[0]:
            if con[0][cur_val][0]=='+':
                con[1]-=(con[0][cur_val][1]*int(var_val))
            else:
                con[1]+=(con[0][cur_val][1]*int(var_val))
            del con[0][cur_val]

    isAssigned, vals = dpll_solver(decision_strat,new_cons,(literal+1))
    if isAssigned:
        vals[cur_var]=var_val
        return True, vals

    var_val = not var_val
    new_cons = [con for con in constraints]
    for con in new_cons:
        if cur_val in con[0]:
            if con[0][cur_val][0]=='+':
                con[1]-=(con[0][cur_val][1]*int(var_val))
            else:
                con[1]+=(con[0][cur_val][1]*int(var_val))
            del con[0][cur_val]

    isAssigned, vals = dpll_solver(decision_strat,new_cons,(literal+1))
    if isAssigned:
        vals[cur_var]=var_val
        return True, vals

    return False, None


def __select_literal(cnf):
    for c in cnf:
        for literal in c:
            return literal[0]

def dpll(cnf, assignments={}):

    if len(cnf) == 0:
        return True, assignments

    if any([len(c)==0 for c in cnf]):
        return False, None

    l = __select_literal(cnf)

    new_cnf = [c for c in cnf if (l, True) not in c]
    new_cnf = [c.difference({(l, False)}) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{l: True}})
    if sat:
        return sat, vals

    new_cnf = [c for c in cnf if (l, False) not in c]
    new_cnf = [c.difference({(l, True)}) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{l: False}})
    if sat:
        return sat, vals

    return False, None



def main():
    print(random.uniform(0,1))


if __name__ == '__main__':
    main()
