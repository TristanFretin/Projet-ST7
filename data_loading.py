import numpy as np
import pandas as pd
import yfinance as yf
import openpyxl as openpyxl
import yaml

# Load config file
with open("config.yaml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)


# Charger le fichier Excel
data = cfg["Tickers_path"]
Mapping = pd.read_excel(data, sheet_name="Mapping")
Tickers = Mapping["Tickers"]
Tickers_list = Tickers.tolist()



# Download the closing prices of the tickers
prices_path = cfg["Prices_path"]
data = yf.download(Tickers_list, start="2010-01-01", end="2024-03-19")["Adj Close"]
data.fillna(method='ffill', inplace=True)
# Replace NaN with 0 only when all the values in the column are NaN
data = data.fillna(0)
data.to_csv(prices_path, index=True)    # Sauvegarde en CSV sans les index








