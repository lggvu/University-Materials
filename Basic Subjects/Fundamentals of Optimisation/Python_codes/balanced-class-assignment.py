from ortools.linear_solver import pywraplp

def input(filename):
    with open(filename) as f:
        [N, M] = [int(x) for x in f.readline().split()] # classes, teachers
        c = [int(x) for x in f.readline().split()] # credits
        L = [] # list of classes that each teacher can teach
        for j in range(M):
            Li = [int(x) for x in f.readline().split()]
            L.append(Li)
        [K] = [int(x) for x in f.readline().split()] # overlapped classes
        F = []
        for k in range(K):
            Fi = [int(x) for x in f.readline().split()]
            F.append(Fi)


        return N, M, c, L, F

## test for input
N, M, c, L, F = input('bca.txt')
# print(f'The total number of classes: N = {N}')
# print(f'The total number of teachers: M = {M}')
# print(f'The credits of each subject: c = {c}')
# print(f'Clases that teachers can teach: L = {L}')
# print(f'Overlapped classes: F = {F}')


# solving the problem
sum_credit = 0
for i in range(N):
    sum_credit += c[i]
solver = pywraplp.Solver.CreateSolver('CBC')
INF = solver.infinity()

x = [[solver.IntVar(0, 1, 'x(' + str(i) + ',' + str(j) + ')') for j in range(M)] for i in range(N)]  # x[i][j]:  teacher j is assigned to class i
y = [solver.IntVar(0, sum_credit, 'y(' + str(j) + ')') for j in range(M)]  # load of teacher i
z = solver.IntVar(0, sum_credit, 'z')  # objective function: the maximum load is minimal

# Constraints
for i in range(N):
    cstr = solver.Constraint(1, 1)  # each subject is assigned to one teacher
    for j in range(M):
        cstr.SetCoefficient(x[i][j], 1)

for j in range(M):
    for i in range(N):
        if i not in L[j]:
            cstr = solver.Constraint(0, 0)  # the teacher is not assigned to a class that he cannot teach
            cstr.SetCoefficient(x[i][j], 1)
# constraints for f
for f in F:
    i = f[0]
    j = f[1]
    for k in range(M):
        cstr = solver.Constraint(0, 1)  # a teacher k cannot teach both classes i and j concurrently
        cstr.SetCoefficient(x[i][k], 1)
        cstr.SetCoefficient(x[j][k], 1)

# constraints on y (load of teacher)
for j in range(M):
    cstr = solver.Constraint(0, 0)  # y = sum(x*c) -> y - sum = 0
    for i in range(N):
        cstr.SetCoefficient(x[i][j], c[i])
    cstr.SetCoefficient(y[j], -1)

# constraint on z - the max wordkload
for j in range(M):
    cstr = solver.Constraint(0, INF)
    cstr.SetCoefficient(z, 1)
    cstr.SetCoefficient(y[j], -1)  # z >= y[j]

# Objective function
obj = solver.Objective()
obj.SetCoefficient(z, 1)
obj.SetMinimization()

rs = solver.Solve()

print(f'The optimal value of maximum workload is: {solver.Objective().Value()}')
print('The list of assigned classes for each teacher:')
for j in range(M):
    for i in range(N):
        if x[i][j].solution_value() == 1:
            print(f'Teacher {j} is assiged to class {i}')

'''
Text file construct:
- The first line contains the total number of classes and teachers
- The second line contains the credits corresponding to each class
- The next three lines contain classes that each teacher can teach
- The next line contains the total number of pairs of overlapped classes
- The remaining lines are the pairs of overlapped classes
'''