from ortools.sat.python import cp_model


class Solver(cp_model.CpModel):

    def __init__(self):
        super().__init__()

        self.solver = cp_model.CpSolver()

        self.input_data("multicast.txt")
        self.define_variables()

    def input_data(self, file_path):
        f = open(file_path)
        self.n_nodes, self.n_edges, self.v_source, self.time_limit = map(int, f.readline().split())
        self.v_source -= 1
        self.times = [[0 for i in range(self.n_nodes)] for j in range(self.n_nodes)]
        self.costs = [[0 for i in range(self.n_nodes)] for j in range(self.n_nodes)]
        self.has_connection = [[False for i in range(self.n_nodes)] for j in range(self.n_nodes)]

        for _ in range(self.n_edges):
            u, v, t, c = map(int, f.readline().split())
            u -= 1
            v -= 1
            self.has_connection[u][v] = True
            self.has_connection[v][u] = True
            self.times[u][v] = t
            self.times[v][u] = t
            self.costs[u][v] = c
            self.costs[v][u] = c

    def define_variables(self):
        N = self.n_nodes
        INF = 9999999999

        # main variables
        self.X = list()
        for i in range(N):
            self.X.append(list())
            for j in range(N):
                if self.has_connection[i][j]:
                    self.X[i].append(self.NewIntVar(0, 1, f"X[{i}, {j}]"))
                else:
                    self.X[i].append(self.NewIntVar(0, 0, f"X[{i}, {j}]"))

        # bool variables
        self.B = list()
        for i in range(N):
            self.B.append(list())
            for j in range(N):
                self.B[i].append(self.NewBoolVar(f"B[{i}, {j}]"))

        # time limit constraints
        self.T = list()
        for i in range(N):
            self.T.append(self.NewIntVar(0, INF, f"T[{i}]"))
            self.Add(self.T[i] <= self.time_limit)
        self.Add(self.T[self.v_source] == 0)

        # add the time used
        for i in range(N):
            for j in range(N):
                self.Add(self.X[i][j] == 1).OnlyEnforceIf(self.B[i][j])
                self.Add(self.T[i] + self.times[i][j] == self.T[j]).OnlyEnforceIf(self.B[i][j])

                self.Add(self.X[i][j] == 0).OnlyEnforceIf(self.B[i][j].Not())

        # income flow
        # v_source is 0 and the other is 1
        for i in range(N):
            if i == self.v_source:
                in_flow = 0
            else:
                in_flow = 1

            self.Add(sum(self.X[j][i] for j in range(N)) == in_flow)

        # outcome flow of v_source must >= 1
        self.Add(sum(self.X[self.v_source][i] for i in range(N)) >= 1)

        self.Minimize(sum(self.X[i][j] * self.costs[i][j] for j in range(N) for i in range(N)))

    def solve(self):
        status = self.solver.Solve(self)
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            print("Objective Value =", self.solver.ObjectiveValue())
            self.print_solution()
        else:
            print("no optimal solution")

    def print_solution(self):
        N = self.n_nodes

        for i in range(N):
            for j in range(N):
                if self.solver.Value(self.X[i][j]) == 1:
                    print(f'{i + 1} -> {j + 1}')


if __name__ == '__main__':
    solver = Solver()
    solver.solve()
