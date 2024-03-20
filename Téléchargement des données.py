
# On doit tomber sur environ 15% de volatilité annualisée.

### Exercice 1

import numpy as np
import pandas as pd
import cvxpy as cvx
import yfinance as yf
#import openpyxl as openpyxl

### Exercice 2

# Charger le fichier Excel
path_1 = "C:/Users/Trist/Documents/Cours 2A - CS/Semestre 8/ST7 - Finance stochastique/Projet ST7/Mapping.csv"
path_2 = "C:/Users/Trist/Documents/Cours 2A - CS/Semestre 8/ST7 - Finance stochastique/Projet ST7/MarketCaps.csv"
path_3 = "C:/Users/Trist/Documents/Cours 2A - CS/Semestre 8/ST7 - Finance stochastique/Projet ST7/Sector.csv"
# Charger le fichier CSV
Mapping = pd.read_csv(path_1, sep=";", skip_blank_lines=False)
MarketCaps = pd.read_csv(path_2, sep=";")
Sector = pd.read_csv(path_3, sep=";")


# Afficher le DataFrame
#print(Mapping)

Tickers = Mapping["Tickers"]
Tickers_list = Tickers.tolist()
print(len(Tickers_list))
#data = yf.download(Tickers_list, start="2002-01-01", end="2024-02-29")
#data.fillna(method='ffill', inplace=True)
#data.to_csv("data_indexed.csv", index=True)    # Sauvegarde en CSV sans les index
#print(data) 






