
import numpy as np
import pandas as pd
import cvxpy as cvx
import yfinance as yf

path = "C:/Users/Trist/Documents/Cours 2A - CS/Semestre 8/ST7 - Finance stochastique/Projet ST7/rendements.csv"
rendements = pd.read_csv(path, sep=",",lineterminator='\n',skip_blank_lines=False)


taille_data = rendements.shape
n_2 = taille_data[0]
k_2 = taille_data[1]


def vérification_rendements_bis():
    colonne = rendements.iloc[:,1]
    colonne = colonne.tolist()
    for i in range (3,n_2-1):
        if (colonne[i-1] == 0):
            rendements.iloc[i, 1] = "erreur"
        elif (isinstance(colonne[i], float) and isinstance(colonne[i-1], float)):
            rendements.iloc[i,1] = colonne[i]/colonne[i-1] - 1
        else : 
            rendements.iloc[i, 1] = "erreur"
    rendements.to_csv("rendements_complets.csv", index=False)
                

vérification_rendements_bis()
#print(data.shape)
#print(type(type("bonjour")))
            
    