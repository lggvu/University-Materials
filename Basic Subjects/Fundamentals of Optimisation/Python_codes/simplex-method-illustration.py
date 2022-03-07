from ortools.linear_solver import pywraplp
from matplotlib import pyplot as plt
import numpy as np

def plot(a1,a2,b,color,style):
    x1 = [0,0]
    x2 = [0,0]
    #plot function a1*x1 + a2*x2 = b
    if a1 == 0:
        x1 = [0,10]
        x2 = [b/a2,b/a2]
        
    elif a2 == 0:
        x1 = [b/a1,b/a1]
        x2 = [0,10]
    else:   
        x1 = np.linspace(0,5,10)
        x2 = (b-a1*x1)*1.0/a2
    
    #print('x1 = ',x1)
    #print('x2 = ',x2)
    fig = plt.plot(x1,x2,color=color,linestyle=style)
    
solver = pywraplp.Solver.CreateSolver('CBC')
INF = solver.infinity()
x1 = solver.NumVar(0,INF,'x1')
x2 = solver.NumVar(0,INF,'x2')

c1 = solver.Constraint(-INF,8)
c1.SetCoefficient(x1,1)
c1.SetCoefficient(x2,2)

c2 = solver.Constraint(-INF,7)
c2.SetCoefficient(x1,2)
c2.SetCoefficient(x2,1)

c3 = solver.Constraint(-INF,2)
c3.SetCoefficient(x1,1)
c3.SetCoefficient(x2,-1)

obj = solver.Objective()
obj.SetCoefficient(x1,-3)
obj.SetCoefficient(x2,-2)

rs_status = solver.Solve()
if rs_status == pywraplp.Solver.OPTIMAL:
    print(solver.Objective().Value())
    print('x1 = ',x1.solution_value(),' x2 = ',x2.solution_value())



plot(1,2,8,'brown','solid')
plot(2,1,7,'green','solid')
#plot(1,1,4)
#plot(0,1,8)
plot(1,-1,2,'blue','solid')
plot(1,0,0,'black','solid')
plot(0,1,0,'black','solid')
plot(3,2,4,'red','dashed')
plot(3,2,10,'red','dashed')
plot(3,2,12,'red','dashed')


plt.show()

