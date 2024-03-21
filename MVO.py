import cvxpy as cp
import numpy as np
import pandas as pd
import yaml



def optimize(mean, cov, risk_aversion):
    w = cp.Variable(len(mean))
    objective = cp.Maximize(mean.T @w)
    constraints = [cp.sum(w) == 1, w >= 0, cp.quad_form(w, cov) <= risk_aversion]
    problem = cp.Problem(objective, constraints)
    problem.solve()
    return w.value, problem.value
    

# Load yaml config file
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)


print("Loading data")
# Load data
sp = pd.read_csv(config["Prices_path"])
sp["Date"] = pd.to_datetime(sp["Date"])
sp.set_index("Date", inplace=True)

print("Data loaded")

# Parameters
number_of_assets = len(sp.columns)
start_date = "2019-01-02"
end_date = "2019-12-31"
months_past = 3
risk_aversion = 0.1

print("Setting up problem")
print("Using data from", start_date, "to", end_date)
print("Using", months_past, "months of past data")
print("Risk aversion:", risk_aversion)
print('Number of assets:', number_of_assets)



# Solve problem for different dates 
dates = pd.date_range(start=start_date, end=end_date, freq="MS")

# Create w dataframe
w = pd.DataFrame(index=dates, columns=sp.columns)

###### TO FIX : SOME STOCKS GO FROM NAN TO SOME VALUE. SINCE WE 
###### WE FILL NAN WITH 0 AND THEN CALCULATE A PERCENTAGE CHANGE
###### WE GET SOME INF VALUES. THIS NEED A SOLUTION

#### WE WILL REPLACE INF VALUES WITH 0

print("Starting solving problem")
for date in dates:
    print("Solving for date", date)
    sp_past_window = sp.loc[pd.to_datetime(date) - pd.DateOffset(months=months_past) : pd.to_datetime(date)]
    sp_past_window_returns = sp_past_window.pct_change().fillna(0) # Account for columns only with Nan
    sp_past_window_returns = sp_past_window_returns.iloc[1:] # drop first line with Nan

    sp_past_window_returns = sp_past_window_returns.replace([np.inf, -np.inf], 0)

    # Mean and covariance matrix
    mean = sp_past_window_returns.mean().values
    cov = sp_past_window.cov().values

    cov_fixed = cov + 0.1 * np.identity(len(mean))

    print("Covariance norm is", np.linalg.norm(cov_fixed))

    # Optimize
    try: 
        weights, objective = optimize(mean, cov_fixed, risk_aversion)
        w.loc[date] = weights
        print("Problem solved successfully")
    except:
        print("Error in solving problem")
        continue


# save w to csv
w.to_csv(config["weights_path"])

    
    


    
