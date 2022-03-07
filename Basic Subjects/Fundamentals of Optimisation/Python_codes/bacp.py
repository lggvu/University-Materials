from ortools.sat.python import cp_model
from time import time


class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback): # print intermediate solution
	def __init__(self,variables):
		cp_model.CpSolverSolutionCallback.__init__(self)
		self.__variables= variables
		self.__solution_count = 0
	def on_solution_callback(self):
		self.__solution_count += 1
		for v in self.__variables:
			print('%s = %i'% (v,self.Value(v)), end = ' ')
			print()
	def solution_count():
		return self.__solution_count

model = cp_model.CpModel()

def inp(filename):
	with open(filename) as f:
		n, m = [int(x) for x in f.readline().split()]
		gam, lam = [int(x) for x in f.readline().split()]
		alpha, bet = [int(x) for x in f.readline().split()]
		c = [int(x) for x in f.readline().split()]
		[k] = [int(x) for x in f.readline().split()]
		preq = []
		for _ in range(k):
			r = [int(x) for x in f.readline().split()]
			preq.append(r)

	return n, m, gam, lam, alpha, bet, c, preq

filename = 'bacp.in31'
n, m, gam, lam, alpha, bet, c, preq = inp(filename)



x = [model.NewIntVar(0, int(m), 'x[' + str(i) + ']') for i in range(n)]
z = [[model.NewIntVar(0, 1, 'z(' + str(i) + ',' + str(j) + ')') for j in range(m)] for i in range(n)]


## Constraints
for p in preq:
	model.Add((x[p[0]-1]) < (x[p[1]-1]))

for j in range(m):
	sum_cre = 0
	sum_course = 0
	for i in range(n):
		sum_cre += z[i][j] * c[i]
		sum_course += z[i][j]
	model.Add(sum_cre >= gam)
	model.Add(sum_cre <= lam)
	model.Add(sum_course >= alpha)
	model.Add(sum_course <= bet)


for i in range(n):
	for j in range(m):
		b = model.NewBoolVar('b')
		model.Add(x[i] == j).OnlyEnforceIf(b)
		model.Add(x[i] != j).OnlyEnforceIf(b.Not())
		model.Add(z[i][j] == 1).OnlyEnforceIf(b)
		model.Add(z[i][j] == 0).OnlyEnforceIf(b.Not())

for i in range(n):
	model.Add(sum([z[i][j] for j in range(m)]) == 1)


if __name__ == '__main__':
	start = time()

	solver = cp_model.CpSolver()
	status = solver.Solve(model)
	solution_printer = VarArraySolutionPrinter(x)
	solver.parameters.enumerate_all_solutions = False
	status = solver.Solve(model, solution_printer)

	end = time()
	print(f'Total execution time: {end-start}s')

