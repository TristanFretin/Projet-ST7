import numpy as np
import cvxpy as cp

cov = np.load("cov.npy")
mean = np.load("mean.npy")

def optimize(mean, cov, risk_aversion):
    w = cp.Variable(len(mean))
    objective = cp.Maximize(mean.T @w)
    constraints = [cp.sum(w) == 1, w >= 0, cp.quad_form(w, cov) <= risk_aversion]
    problem = cp.Problem(objective, constraints)
    problem.solve(verbose=True)
    return w.value, problem.value
    

optimize(mean, cov, 0.1)