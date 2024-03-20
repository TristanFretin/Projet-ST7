import numpy as np
import pandas as pd
import yfinance as yf
import openpyxl as openpyxl



# Charger le fichier Excel
data = "data/DataProjets.xlsx"
Mapping = pd.read_excel(data, sheet_name="Mapping")
Tickers = Mapping["Tickers"]
Tickers_list = Tickers.tolist()



# Download the data
data = yf.download(Tickers_list, start="20014-01-01", end="2024-02-29")
data.fillna(method='ffill', inplace=True)
data.to_csv("data/data_indexed.csv", index=True)    # Sauvegarde en CSV sans les index








