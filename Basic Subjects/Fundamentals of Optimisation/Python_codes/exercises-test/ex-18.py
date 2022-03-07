# Exercise 18
from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

x1 = solver.NumVar(0, solver.infinity(), 'x1')
x2 = solver.NumVar(0, solver.infinity(), 'x2')
x3 = solver.NumVar(0, solver.infinity(), 'x3')
x4 = solver.NumVar(0, solver.infinity(), 'x4')
x5 = solver.NumVar(0, solver.infinity(), 'x5')


'''
Defining the constraints
'''
solver.Add(x1 + x2 + x3 + x4 + x5 == 5)
solver.Add(x1 + x2 + 2*x3 + 2*x4 + 2*x5 == 8)
solver.Add(x1 + x2 == 2)
solver.Add(x3 + x4 + x5 == 3)

'''
Defining the objective function
'''
solver.Minimize(2*x1 + x2 + x3)

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print('Solution:')
    print('Objective value =', solver.Objective().Value())
    print('x1 =', x1.solution_value())
    print('x2 =', x2.solution_value())
    print('x3 =', x3.solution_value())
    print('x4 =', x4.solution_value())
    print('x5 =', x5.solution_value())

else:
    print('The problem does not have an optimal solution.')