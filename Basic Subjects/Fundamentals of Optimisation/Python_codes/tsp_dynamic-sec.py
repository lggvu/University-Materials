from ortools.linear_solver import pywraplp
import numpy as np
import random
import time


def inp(filename):
    with open(filename) as f:
        [n] = [int(x) for x in f.readline().split()]  # number of vertices
        d = []
        for _ in range(n):
            r = [int(x) for x in f.readline().split()]
            d.append(r)
    d = np.array(d, dtype=int)
    return n, d


# randomised input
def generate_inp(filename, n):
    f = open(filename, 'w')
    f.write(str(n) + '\n')
    for i in range(n):
        line = ''
        for j in range(n):
            w = random.randint(1, 100)
            if i == j:
                w = 0
            line = line + str(w) + ' '
            f.write(str(w) + ' ')
        f.write('\n')
    f.close()

filename = 'tsp-48.txt'
# generate_inp(filename, 100)

n, d = inp(filename)
print('d = ', d)
print('n = ', n)

'''
Dynamic SEC
'''


def solver_var():  # create solver and variables
    solver = pywraplp.Solver.CreateSolver('CBC')
    x = [[solver.IntVar(0, 1, 'x(' + str(i) + ',' + str(j) + ')') for i in range(n)] for j in range(n)]
    x = np.array(x)
    return solver, x


def bf_constraint(solver, x):  # balance flow constraint
    for i in range(n):
        cstr = solver.Constraint(1, 1)
        for j in range(n):
            if i != j:
                cstr.SetCoefficient(x[i, j], 1)
        cstr = solver.Constraint(1, 1)
        for j in range(n):
            if i != j:
                cstr.SetCoefficient(x[j, i], 1)


def solve_dynamic(SEC):  # solve with dynamic SEC
    solver, x = solver_var()
    bf_constraint(solver, x)

    # create SE-constraint for all elements in the list SEC
    for C in SEC:
        cstr = solver.Constraint(0, len(C) - 1)
        for i in C:
            for j in C:
                if i != j:
                    cstr.SetCoefficient(x[i, j], 1)

    obj = solver.Objective()  # Objective function
    for i in range(n):
        for j in range(n):
            if i != j:
                obj.SetCoefficient(x[i, j], int(d[i, j]))

    solver.Solve()

    temp = np.array([[0 for _ in range(n)] for _ in range(n)])
    for i in range(n):
        for j in range(n):
            if i != j and x[i, j].solution_value() > 0:
                temp[i, j] = 1
    return temp, solver.Objective().Value()


def find_next(s, temp):
    for i in range(n):
        if i != s and temp[s, i] == 1:  # i is a solution of dynamic SEC
            return i
    return -1


def extract_cycle(s, temp):
    C = list()
    C.append(s)
    while True:
        node = find_next(s, temp)
        if node == -1:
            # return None
            pass 
        if node in C:
            return C
        C.append(node)
        s = node  # node becomes the next start

    return None


def solve_tsp():
    SEC = []
    while True:
        temp, opt = solve_dynamic(SEC)  # enforce constaints
        print('Objective value: ', opt)

        # find subtours of solutions
        mark = [False for _ in range(n)]
        for s in range(n):
            if mark[s] is False:
                C = extract_cycle(s, temp)  # list of points
                print(f'Subtour {C} with length = {len(C)}')
                if len(C) == n:
                    print('OPTIMAL SOLUTION FOUND: ', opt)
                    return C  # optimal solution found (global tour)

                SEC.append(C)
                for v in C:
                    mark[v] = True  # visited subtours

# def print_sol_x(x):
#     path = list()
#     for i in range(n):
#         for j in range(n):
#             if x[i][j].solution_value() == 1:
#                 path.append(i)
#     print(*path, sep=' -> ', end=' -> %s\n' % path[0])
#
# def print_sol_temp(temp):
#     path2 = list()
#     for i in range(n):
#         for j in range(n):
#             if temp[i][j].solution_value() == 1:
#                 path2.append(i)
#     print(*path2, sep=' -> ', end=' -> %s\n' % path2[0])

if __name__ == '__main__':
    start = time.time()
    solve_tsp()
    end = time.time()
    print(f'Total excution time = {end - start}s for the dataset of {n} cities')