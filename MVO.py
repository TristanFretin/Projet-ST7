import cvxpy as cp
import numpy as np
import pandas as pd
import yaml
import matplotlib.pyplot as plt
import seaborn as sns
import tqdm as tqdm

sns.set_theme()

with open("config.yaml", "r") as stream:
    config = yaml.safe_load(stream)


# Load the prices dataframe
prices = pd.read_csv(config["Prices_data"]["save_path"], index_col=0)
market_cap = pd.read_excel(config["Project_data"]["load_path"], index_col=0, sheet_name=config["Project_data"]["market_caps"])

Mapping = pd.read_excel(config["Project_data"]["load_path"],sheet_name="Mapping")
sedols_to_tickers = dict(zip(Mapping["Sedol"], Mapping["Tickers"]))

# Rename the columns to tickers
market_cap.columns = [sedols_to_tickers[sedol] for sedol in market_cap.columns]

benchmark = pd.read_csv("data/index.csv", index_col=0)

# Calculate the returns
returns = prices.pct_change()
# replace inf values with nan
returns.replace([np.inf, -np.inf], np.nan, inplace=True)
returns.fillna(0, inplace=True)

# Take the mean by month
returns.index = pd.to_datetime(returns.index)
returns = returns.resample("M").mean()

# Remove tickers with weird returns
returns[["KRI", "BOL", "BLS", "CIN", "PBG", "SOV", "BMC", "HNZ", "EP"]] = 0

# Calculate the covariance matrix
mean_returns_all = returns.mean()
std_returns_all = returns.std()

cov_matrix = returns.cov()

# print(market_cap.mean().head())

# Plot a scatter plot of mean vs std with hue being the market cap
# plt.figure()
# sns.scatterplot(x=std_returns_all, y=mean_returns_all, hue=market_cap.mean(),size = market_cap.mean(), sizes = (20,200) , palette="viridis")
# plt.xlabel("Standard deviation")
# plt.ylabel("Mean return")
# plt.title("Mean return vs Standard deviation")



# Optimize the portfolio
mean_returns_all_numpy = mean_returns_all.to_numpy()
cov_matrix_numpy = cov_matrix.to_numpy()

def optimize(mean, cov, risk_aversion):
    w = cp.Variable(len(mean))
    objective = cp.Maximize(mean.T @ w)
    constraints = [cp.sum(w) == 1, w >= 0, cp.quad_form(w, cov) <= risk_aversion]
    problem = cp.Problem(objective, constraints)
    problem.solve()
    return w.value, problem.value

w_risky, _ = optimize(mean_returns_all_numpy, cov_matrix_numpy, 1e-8)
w_very_risky, _ = optimize(mean_returns_all_numpy, cov_matrix_numpy, 1e-5)
w_very_very_risky, _ = optimize(mean_returns_all_numpy, cov_matrix_numpy, 1e-2)


# Create the portfolio with three columns for the three different portfoliosù
portfolio = pd.DataFrame(index=prices.index, columns=["Very very risky", "Very risky", "Risky"])

for date in portfolio.index:
    portfolio["Very very risky"].loc[date] = np.dot(w_very_very_risky, prices.loc[date].values)
    portfolio["Very risky"].loc[date] = np.dot(w_very_risky, prices.loc[date].values)
    portfolio["Risky"].loc[date] = np.dot(w_risky , prices.loc[date].values)



portfolio.index = pd.to_datetime(portfolio.index)
portfolio = portfolio.resample("M").mean()

benchmark.index = pd.to_datetime(benchmark.index)
benchmark = benchmark.resample("M").mean()



# Plot the portfolio and the benchmark
plt.figure()
plt.plot(portfolio["Very very risky"], label="Portfolio Very Very risky")
plt.plot(portfolio["Very risky"], label="Portfolio Very risky")
plt.plot(portfolio["Risky"], label="Portfolio Riksy")
plt.plot(benchmark, label="Benchmark")
plt.legend()
plt.show()
# plt.savefig("graphs/Portfolio.png")

# Show the number of weights bigger than 1e-5
print("For the very risky portfolio the number of weights bigger than 1e-3 is:", np.sum(w_risky > 1e-3))
print("For the very very risky portfolio the number of weights bigger than 1e-3 is:", np.sum(w_very_risky > 1e-3))
print("For the very very very risky portfolio the number of weights bigger than 1e-4 is:", np.sum(w_very_very_risky > 1e-3))

print("For compaison the number of weights bigger than 1e-3 in the market cap is:", np.sum(market_cap.mean() > 1e-3))