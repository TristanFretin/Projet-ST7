

# On doit tomber sur environ 15% de volatilité annualisée.

### Exercice 1

import numpy as np
import pandas as pd
import cvxpy as cvx
import yfinance as yf
#import openpyxl as openpyxl

### Exercice 2

path = "C:/Users/Trist/Documents/Cours 2A - CS/Semestre 8/ST7 - Finance stochastique/Projet ST7/rendements_complets.csv"
rendements_complets = pd.read_csv(path, sep=",",lineterminator='\n',skip_blank_lines=False, low_memory=False)
chemin_fichier_excel = "C:/Users/Trist/Documents/Cours 2A - CS/Semestre 8/ST7 - Finance stochastique/Projet ST7/DataProjets.xlsx"
xls = pd.ExcelFile(chemin_fichier_excel)
#Tickers = pd.read_excel(xls, "Mapping")
#Tickers = Tickers.iloc[1:,1]
#Tickers = Tickers.tolist()
#print(len(Tickers))
#print(Tickers)

#Tickers_rendements_complets = rendements_complets.iloc[0,1:]
#Tickers_rendements_complets = Tickers_rendements_complets.tolist()
#print(Tickers_rendements_complets)
#lst_indexes = [0]
#for i in range (len(Tickers_rendements_complets)):
#    if Tickers_rendements_complets[i] in Tickers :
#        lst_indexes.append(i+1)

#print(lst_indexes)
rendements_réduits = rendements_complets.iloc[:,0:562]
print(rendements_réduits.shape)
rendements_réduits.to_csv("rendements_réduits.csv", index=False)








