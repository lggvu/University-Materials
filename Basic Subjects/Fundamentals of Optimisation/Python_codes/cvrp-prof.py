from ortools.linear_solver import pywraplp


def input(filename):
    with open(filename) as f:
        N, K = [int(x) for x in f.readline().split()]
        c = [int(x) for x in f.readline().split()]
        r = [int(x) for x in f.readline().split()]
        d = [[int(x) for x in f.readline().split()] for _ in range(N + 2 * K)]
    return N, K, c, r, d


N, K, c, r, d = input('cvrp-N4-K2.txt')
for _ in range(2 * K):
    r.append(0)  # expand r to the size of 2*k

print('Number of customers: N =', N)
print('Number of trucks: k = ', K)
print('Capacity: c =', c)
print('Requested items: r =', r)
print('Distance matrix: ', d)

A = []
# flow from i to j
for i in range(N + 2 * K):
    for j in range(N + 2 * K):
        if (j not in range(N, N + K)) and (i not in range(N + K, N + 2 * K)) and (i != j):
        # j cannot be the starting point, and i cannot be the terminal point, and no loops at one node
            A.append([i, j])

Ao = lambda x: (j for i, j in A if i == x)  # A-out
Ai = lambda x: (i for i, j in A if j == x)  # A-in


print('A = ', A)

total_demand = sum(r)
M = total_demand + max(r)  # big constant

solver = pywraplp.Solver('CVRP_MIP', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
INF = solver.infinity()

# DECISION VARIABLES
x = [[[solver.IntVar(0, 1, f'x[{k}][{i}][{j}]') for j in range(N + 2 * K)] for i in range(N + 2 * K)] for k in range(K)]  # x = 1 if the truck K traverses from point i to point j, 0 otherwise

y = [solver.IntVar(0, total_demand, f'y[{i}]') for i in range(N + 2 * K)]  # accumulated load until the point i

z = [solver.IntVar(0, K, f'z[{i}]') for i in range(N + 2 * K)]  # index of the truck passing the point i

# each truck comes in and out a point once
for i in range(N):
    cstr = solver.Constraint(1, 1)
    for k in range(K):
        for j in Ao(i):
            cstr.SetCoefficient(x[k][i][j], 1)

for i in range(N):
    cstr = solver.Constraint(1, 1)
    for k in range(K):
        for j in Ai(i):
            cstr.SetCoefficient(x[k][j][i], 1)

for i in range(N):  # the incoming truck and outgoing truck at the point i is the same
    for k in range(K):
        cstr = solver.Constraint(0, 0)
        for j in Ao(i):
            cstr.SetCoefficient(x[k][i][j], 1)
        for j in Ai(i):
            cstr.SetCoefficient(x[k][j][i], -1)

for k in range(K):
    cstr = solver.Constraint(1, 1)
    for j in range(N):
        cstr.SetCoefficient(x[k][k + N][j], 1)

    cstr = solver.Constraint(1, 1)
    for j in range(N):
        cstr.SetCoefficient(x[k][j][k + K + N], 1)

    # the accumulated load does not exceed the maximum capacity
    cstr = solver.Constraint(0, c[k])
    cstr.SetCoefficient(y[k + K + N], 1)

    # one truck, one path
    cstr = solver.Constraint(k, k)
    cstr.SetCoefficient(z[k + K + N], 1)

    cstr = solver.Constraint(k, k)
    cstr.SetCoefficient(z[k + N], 1)

for k in range(K):
    for i, j in A:  # accumulated at j = load accumulated at i + r(j)
        cstr = solver.Constraint(-M + r[j], INF)
        cstr.SetCoefficient(x[k][i][j], -M)
        cstr.SetCoefficient(y[j], 1)
        cstr.SetCoefficient(y[i], -1)

        cstr = solver.Constraint(-M - r[j], INF)
        cstr.SetCoefficient(x[k][i][j], -M)
        cstr.SetCoefficient(y[j], -1)
        cstr.SetCoefficient(y[i], 1)

    for i, j in A:  # index of truck(i) = index of truck(j)
        cstr = solver.Constraint(-M, INF)
        cstr.SetCoefficient(x[k][i][j], -M)
        cstr.SetCoefficient(z[j], 1)
        cstr.SetCoefficient(z[i], -1)

        cstr = solver.Constraint(-M, INF)
        cstr.SetCoefficient(x[k][i][j], -M)
        cstr.SetCoefficient(z[j], -1)
        cstr.SetCoefficient(z[i], 1)

for k in range(K):
    c = solver.Constraint(0, 0)
    c.SetCoefficient(y[k + N], 1)  # initial load = 0

# OBJECTIVE FUNCTION
obj = solver.Objective()
for k in range(K):
    for i, j in A:
        obj.SetCoefficient(x[k][i][j], d[i][j])
obj.SetMinimization()

rs = solver.Solve()

print(f'Optimal objective value = {obj.Value()}')

# PRINT TRUCK ROUTE
def findNext(k, i):
    for j in Ao(i):
        if x[k][i][j].solution_value() > 0:  # j is the next point to arrive
            return j


def route(k):  # construct a complete route
    s = ''
    i = k + N
    while i != (k + K + N):
        s = s + str(i) + ' -> '
        i = findNext(k, i)
    s = s + str(k + K + N)
    return s

if __name__ == '__main__':
    print()
    print('Solving Started...'  )
    for k in range(K):
        print(f'route[{k}] = {route(k)}, y = {y[k+K+N].solution_value()}')
        for i, j in A:
            if x[k][i][j].solution_value() > 0:
                print(f'({i} -> {j})')
