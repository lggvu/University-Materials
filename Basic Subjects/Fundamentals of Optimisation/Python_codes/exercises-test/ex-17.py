# Exercise 17
from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

x1 = solver.NumVar(0, solver.infinity(), 'x')
x2 = solver.NumVar(0, solver.infinity(), 'y')

'''
Defining the constraints
'''
# Constraint 1: 2x1 + x2 <= 8
solver.Add(2 * x1 + x2 <= 8.0)

# Constraint 2: x1 + 3x2 <= 9
solver.Add(x1 + 3 * x2 <= 9.0)

'''
Defining the objective function
'''
solver.Maximize(2 * x1 + 3 * x2)

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print('Solution:')
    print('Objective value =', solver.Objective().Value())
    print('x1 =', x1.solution_value())
    print('x2 =', x2.solution_value())
else:
    print('The problem does not have an optimal solution.')





