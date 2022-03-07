'''
f(x) = 2x1 + 4x2 - x3 -> min
    -INF <= 4x1 - x2 + 2x3 <= 7  (c1)
    x1 + x2 + x3 = 5  (c2)
    -INF <= 3x1 + x2 - 2x3 <= 10
    x1, x2 real numbers, x1, x2 >= 2
    x3: integer, 0 <= x3 <= 10
'''

from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

INF = solver.infinity()

x1 = solver.NumVar(2, INF, 'x[1]')
x2 = solver.NumVar(2, INF, 'x[2]')
x3 = solver.IntVar(0, 10, 'x[3]')

c1 = solver.Constraint(-INF, 7)
c1.SetCoefficient(x1, 4)
c1.SetCoefficient(x2, -1)
c1.SetCoefficient(x3, 2)

c2 = solver.Constraint(5, 5)
c2.SetCoefficient(x1, 1)
c2.SetCoefficient(x2, 1)
c2.SetCoefficient(x3, 1)

c3 = solver.Constraint(-INF, 10)
c3.SetCoefficient(x1, 3)
c3.SetCoefficient(x2, 1)
c3.SetCoefficient(x3, -2)

obj = solver.Objective()  # objective function
obj.SetCoefficient(x1, 2)
obj.SetCoefficient(x2, 4)
obj.SetCoefficient(x3, -1)

result_status = solver.Solve()

if result_status != pywraplp.Solver.OPTIMAL:
    print('Cannot find the optimal solution')
else:
    print('Optimal objective value is: ', solver.Objective().Value())

print(f'x1 = {x1.solution_value():.4f}\n'
      f'x2 = {x2.solution_value():.4f}\n'
      f'x3 = {x3.solution_value():.4f}')


