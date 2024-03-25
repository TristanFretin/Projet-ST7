import pandas as pd
import yaml
import matplotlib.pyplot as plt

# Load config file
with open("config.yaml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

# Price loading
prices = pd.read_csv(cfg["Prices_path"], index_col=0)
prices.index = pd.to_datetime(prices.index)   

# Load market cap and set index to date
market_cap = pd.read_excel(cfg["Tickers_path"], sheet_name="MarketCaps")
market_cap = market_cap.set_index("Date")
market_cap.index = pd.to_datetime(market_cap.index)

# Dictionnaire de correspondance pour les sedols to tickers
correspondance = pd.read_excel(cfg["Tickers_path"], sheet_name="Mapping")
sedols_to_tickers = correspondance[["Sedol", "Tickers"]]
sedol_to_ticker = dict(zip(sedols_to_tickers["Sedol"], sedols_to_tickers["Tickers"]))

market_cap.columns = [sedol_to_ticker[col] for col in market_cap.columns]

market_cap = market_cap.resample('D').ffill()

cutoff_day_start = prices.index[0]
cutoff_day_end = prices.index[-1]

market_cap = market_cap[market_cap.index >= cutoff_day_start]
market_cap = market_cap[market_cap.index <= cutoff_day_end]
 

df_merged = pd.merge(market_cap, prices, on='Date', how='inner')

result = pd.DataFrame(index=df_merged.index)

for stock in prices.columns:
    result[stock] = df_merged[stock + "_x"] * df_merged[stock + "_y"]

index = 21 * result.sum(axis=1) # tkt 

# Rename the column 0 to sp
index = index.rename("SP")

# Save the SP 300 index
index.to_csv(cfg["index_path"])


# Create a figure for the SP 300 hunder index
plt.figure()
plt.plot(index)
plt.title("SP 300 Index")
plt.ylabel("Indice boursier")
plt.xlabel("Date")
plt.grid()
plt.savefig(cfg["graphs_path"] + "indice_boursier.png", dpi=1000)


