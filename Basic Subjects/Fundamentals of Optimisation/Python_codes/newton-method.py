# Problem: f(x1, x2, x3) = x1^2 + x2^2 + x3^2 - x1x2 - x2x3 + x1 + x3 -> min?

import numpy as np

def newton(f, df, Hf, x0):  # (objective function, gradient, Hessian, initialiser)
    x = x0  # initialiser
    for i in range(1000):
        iH = np.linalg.inv(Hf(x))  # inverse of Hessian matrix
        D = np.array(df(x)).T  # transpose of gradient (from list to column)
        h = iH.dot(D)
        if np.linalg.norm(h) == 0:
            print(f'Result: {f(x)}\n'
                  f'Total steps taken: {i}')
            break
        x = x - h
        print(f'Step {i}: {x},\n'
              f'f={f(x)}')

f = lambda x: x[0]**2 + x[1]**2 + x[2]**2 - x[0]*x[1] - x[1]*x[2] + x[0] + x[2]
df = lambda x: [2*x[0]- x[1] + 1, -x[0] + 2*x[1] - x[2], 2*x[2] - x[1] + 1]
Hf = lambda x: [[2, -1, 0], [-1, 2, -1], [0, -1, 2]]
x0 = np.array([0, 0, 0]).T
newton(f, df, Hf, x0)

