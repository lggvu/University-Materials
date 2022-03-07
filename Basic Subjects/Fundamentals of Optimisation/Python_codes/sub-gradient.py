# Problem: minimise f(x), where f(x) = max(a_i(x)^T + b_i), i=1,...,m
# -> Finding subgradient: given x, the index j for which:
# a_j(x)^T + bj = max(a_i(x)^T + b_i), i=1,...,m
# -> Subgradient at x is g=a_j

import numpy as np

def solve(A, b):
    f = lambda x: np.max(A.dot(x) + b)
    sg = lambda x: A[np.argmax(A.dot(x) + b)]  # subgradient equation
    x0 = [0, 0]
    x = np.array(x0).T
    f_best = f(x)
    for i in range(int(1e6)):
        alpha = .1
        x = x - alpha * sg(x)
        if f_best > f(x):
            f_best = f(x)
        if i % 10000 == 0:
            print(f'Step {i}, f={f(x)}, f_best={f_best}')
    return f_best


A = np.array([[1, 2], [-2, -1], [-3, 2], [1, -1]])
b = np.array([3, 4, 5, 1]).T
rs = solve(A, b)
print('Result = ', rs)
