import cvxpy as cp
import numpy as np
import pandas as pd
import yaml

# Load yaml config file
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Load data
sp = pd.read_csv(config["Prices_path"])
sp["Date"] = pd.to_datetime(sp["Date"])
sp.set_index("Date", inplace=True)


date = "2019-01-02"
months_past = 3

def optimize(mean, cov_fixed, risk_aversion=0.10):
    # Is covariance matrix positive definite? Check if all eigenvalues are positive
    for eig in np.linalg.eigvals(cov_fixed):
        if eig <= 0:
            print("Covariance matrix is not positive definite")
            break

    w = cp.Variable(len(mean))
    objective = cp.Maximize(mean.T @ w)
    constraints = [cp.sum(w) == 1, w >= 0, cp.quad_form(w, cov_fixed) <= risk_aversion]
    prob = cp.Problem(objective, constraints)
    prob.solve()

    return w.value, prob.value

sp_past_window = sp.loc[pd.to_datetime(date) - pd.DateOffset(months=months_past) : pd.to_datetime(date)]
sp_past_window_returns = sp_past_window.pct_change().fillna(0) # Account for columns only with Nan
sp_past_window_returns = sp_past_window_returns.iloc[1:] # drop first line with Nan

# Mean and covariance matrix
mean = sp_past_window_returns.mean().values
cov = sp_past_window.cov().values

cov_fixed = cov + 0.1 * np.identity(len(mean))

weights, value = optimize(mean, cov_fixed)

print(value)

