from ortools.linear_solver import pywraplp


def input(filename):
    with open(filename) as f:
        V, E, s, l = [int(x) for x in f.readline().split()]
        s -= 1
        adj, cost, time, temp_adj = [], [], [], []
        temp = [[int(x) for x in f.readline().split()] for _ in range(E)]

        for i in range(len(temp)):
            temp_adj.append(temp[i][0:2])
            adj = [[int(x-1) for x in k] for k in temp_adj]
            cost.append(int(temp[i][2]))
            time.append(int(temp[i][3]))
    return V, E, s, l, adj, cost, time


filename = 'multicast.txt'
V, E, s, l, adj, cost, time = input(filename)
print(f'Number of vertices V = {V}, edges E = {E}')
print('Start node:', s)
print('Maximum latency: l =', l)
print(f'Pair of adjacent nodes: {adj}')
print(f'Transmission cost: {cost}')
print(f'Transmission time: {time}')


solver = pywraplp.Solver('MRP_MIP', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
INF = solver.infinity()

# DECISION VARIABLES
x = [[solver.IntVar(0, 1, f'x({i}, {j})') for j in range(V)] for i in range(V)]
y = [solver.IntVar(0, l, f'y({i}') for i in range(V)]

adj_dict = {}

for pair in adj:
    adj_dict[pair[0]] = adj_dict.get(pair[0], [])
    adj_dict[pair[0]].append(pair[1])

print("Adjacency dictionary:", adj_dict)

# CONSTRAINTS
for terminal in adj_dict.values():  # each node gets only one transmission from one other node
    for j in terminal:
        cstr = solver.Constraint(1, 1)
        for i in adj_dict.keys():
            if i != s:
                cstr.SetCoefficient(x[i][j], 1)

for start in adj_dict.keys():  # start node will transmit to at least one other node
    if start == s:
        cstr = solver.Constraint(1, INF)
        for i in adj_dict[start]:
            cstr.SetCoefficient(x[start][i], 1)

sum_time = sum(time)
M = sum_time + l  # big constant

for i in adj_dict.keys():
    for j in adj_dict[i]:
        index = adj.index([i, j])
        cstr = solver.Constraint(-M, -M)
        cstr.SetCoefficient(y[i], -1)
        cstr.SetCoefficient(x[i][j], -M)
        cstr.SetCoefficient(y[j], 1)
        cstr.SetCoefficient(time[index], -1)


# SEC
# generating subtours
b = [0 for _ in range(V)] # b[i] = 1 if i belongs to the subset
def subtour(b):
    i = V - 1
    while i >= 0 and b[i] == 1:
        i -= 1
    if i < 0:
        return None
    b[i] = 1
    for j in range(i+1, V):
        b[j] = 0
    return b


stop = False
while not stop:
    b = subtour(b)
    if b == None:
        stop = True
        break

    s = sum(b)

    if s > 1 and s < V:
        cstr = solver.Constraint(0, s-1)
        for i in adj_dict.keys():
            for j in adj_dict[i]:
                if b[i] == 1 and b[j] == 1:
                    cstr.SetCoefficient(x[i][j], 1)

# OBJECTIVE FUNCTION
obj = solver.Objective()
for i in adj_dict.keys():
    for j in adj_dict[i]:
        index = adj.index([i, j])
        obj.SetCoefficient(x[i][j], cost[index])

obj.SetMinimization()

rs = solver.Solve()

print(f'Optimal objective value = {obj.Value()}')

if __name__ == '__main__':
    print()
    print('Solving Started...')
    for i in adj_dict.keys():
        for j in adj_dict[i]:
            if x[i][j].solution_value() > 0:
                print(f'{i+1} -> {j+1}')