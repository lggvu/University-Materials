from ortools.sat.python import cp_model

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

x = [model.NewIntVar(1, 5, 'x[' + str(i) + ']') for i in range(5)]

c1 = model.Add(x[2] + 3 != x[1])
c2 = model.Add(x[3] <= x[4])
c3 = model.Add(x[2] + x[3] == x[0] + 1)
c4 = model.Add(x[4] <= 3)
c5 = model.Add(x[1] + x[4] == 7)

b = model.NewBoolVar('b')
model.Add(x[2] == 1).OnlyEnforceIf(b)
model.Add(x[2] != 1).OnlyEnforceIf(b.Not())
model.Add(x[4] != 2).OnlyEnforceIf(b)


solver = cp_model.CpSolver()
solution_printer = VarArraySolutionPrinter(x)
solver.SearchForAllSolutions(model, solution_printer)