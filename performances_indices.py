import pandas as pd
import yaml

# Load yaml config file
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Load data
sp = pd.read_csv(config["index_path"])
sp.set_index("Date", inplace=True)
sp.index = pd.to_datetime(sp.index)


# For each year obtain the sp value at the end of the year
years = sp.index.year.unique()
sp_end_year = pd.DataFrame(index=years, columns=["sp"])
for year in years:
    sp_end_year.loc[year, "sp"] = sp.loc[sp.index.year == year].iloc[-1]["SP"]


# Calculate CAGR for each year 
cagr = pd.DataFrame(index=years, columns=["cagr"])
for year in years[1:]:
    cagr.loc[year, "cagr"] = (sp_end_year.loc[year, "sp"] / sp_end_year.loc[year-1, "sp"]) - 1


# Calculate global CAGR
global_cagr = (sp_end_year.loc[years[-1], "sp"] / sp_end_year.loc[years[0], "sp"]) ** (1 / (years[-1] - years[0])) - 1


# Calculate annualized volatility by year
annualized_volatility = pd.DataFrame(index=years, columns=["annualized_volatility"])
for year in years:
    annualized_volatility.loc[year, "annualized_volatility"] = sp.loc[sp.index.year == year]["SP"].pct_change().std() * (252 ** 0.5)


# Calculate global annualized volatility
global_annualized_volatility = sp["SP"].pct_change().std() * (252 ** 0.5)

# Calculate maximum drawdown
sp["cummax"] = sp["SP"].cummax()
sp["drawdown"] = sp["SP"] / sp["cummax"] - 1
max_drawdown = sp["drawdown"].min()

# Calculate second maximum drawdown
sp["drawdown"] = sp["drawdown"].abs()
second_max_drawdown = - sp["drawdown"].nlargest(2).iloc[-1]

# Calculate the number of days to recover from the maximum drawdown
max_drawdown_date = sp["drawdown"].idxmin()


# Valuate at risk quotidienne à 95%
var_95 = sp["SP"].pct_change().quantile(0.05)

# Expected Shortfall quotidien à 95%
sorted_returns = sp['SP'].pct_change().sort_values()
expected_shortfall = sorted_returns.iloc[:int(len(sorted_returns) * 0.05)].mean()

# Pretty print of everything

print(f"Global CAGR: {global_cagr}")
print(f"Global annualized volatility: {global_annualized_volatility}")
print(f"Maximum drawdown: {max_drawdown}")
print(f"Second maximum drawdown: {second_max_drawdown}")
print(f"Value at risk at 95%: {var_95}")
print(f"Expected shortfall at 95%: {expected_shortfall}")
print("\n")
print("Yearly performances:")
print(cagr)
print("\n")
print("Annualized volatility by year:")
print(annualized_volatility)
print("\n")


