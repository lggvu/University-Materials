from ortools.linear_solver import pywraplp
import numpy as np
import random


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
            w = random.randint(1, 10)
            if i == j:
                w = 0
            line = line + str(w) + ' '
            f.write(str(w) + ' ')
        f.write('\n')
    f.close()


generate_inp('tsp-inp.txt', 13)

n, d = inp('tsp-inp.txt')
print('d = ', d)
print('n = ', n)

# generating subtours
b = [0 for _ in range(n)] # b[i] = 1 if i belongs to the subset
def subtour(b):
    i = n - 1
    while i >= 0 and b[i] == 1:
        i -= 1
    if i < 0:
        return None
    b[i] = 1
    for j in range(i+1, n):
        b[j] = 0
    return b

solver = pywraplp.Solver.CreateSolver('CBC')
INF = solver.infinity()

# decision variables
x = [[solver.IntVar(0, 1, 'X(' + str(i) + ',' + str(j) + ')') for i in range(n)] for j in range(n)]

# constraints
for i in range(n):
    cstr = solver.Constraint(1, 1)
    for j in range(n):
        if i != j:
            cstr.SetCoefficient(x[i][j], 1)

for i in range(n):
    cstr = solver.Constraint(1, 1)
    for j in range(n):
        if i != j:
            cstr.SetCoefficient(x[j][i], 1)

# sec
stop = False
while not stop:
    b = subtour(b)
    if b == None:
        stop = True
        break

    s = sum(b)

    if s > 1 and s < n:
        cstr = solver.Constraint(0, s-1)
        for i in range(n):
            for j in range(n):
                if i != j and b[i] == 1 and b[j] == 1:
                    cstr.SetCoefficient(x[i][j], 1)

# objective function
obj = solver.Objective()
for i in range(n):
    for j in range(n):
            obj.SetCoefficient(x[i][j], int(d[i][j]))


obj.SetMinimization()

rs = solver.Solve()

print(f'The optimal value is: {solver.Objective().Value()}')
print('The optimal path is: ')
path = []
for i in range(n):
    for j in range(n):
        if x[i][j].solution_value() == 1:
            print(x[i][j])
            path.append(i)

print(*path, sep=' -> ', end=' -> %s\n' % path[0])


'''
X(1,0)
X(3,1)
X(0,2)
X(2,3)
'''


'''
The current subtour elimination algorithm is not efficient for large inputs
-> Use Dynamic SEC
'''