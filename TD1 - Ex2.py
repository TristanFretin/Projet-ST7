
import numpy as np
import pandas as pd
import cvxpy as cvx
import yfinance as yf

path = "C:/Users/Trist/Documents/Cours 2A - CS/Semestre 8/ST7 - Finance stochastique/Projet ST7/data_indexed.csv"
path_2 = "C:/Users/Trist/Documents/Cours 2A - CS/Semestre 8/ST7 - Finance stochastique/Projet ST7/MarketCaps.csv"
data = pd.read_csv(path, sep=",",lineterminator='\n',skip_blank_lines=False)
#MarketCaps = pd.read_csv(path_2, sep=";")
chemin_fichier_excel = "C:/Users/Trist/Documents/Cours 2A - CS/Semestre 8/ST7 - Finance stochastique/Projet ST7/DataProjets.xlsx"
xls = pd.ExcelFile(chemin_fichier_excel)

liste_dataframes = []
for nom_feuille in xls.sheet_names:
    # Chargez chaque feuille dans un DataFrame séparé
    df = pd.read_excel(xls, nom_feuille)
    liste_dataframes.append(df)

MarketCaps = liste_dataframes[1]

taille = MarketCaps.shape
n = taille[0]       # Nombre de lignes du dataframe MarketCaps
k = taille[1]       # Nombre de colonnes du dataframe MarketCaps

#print(data)

# On vérifie que la somme des poids est bien égale à 1 pour chaque mois.

def vérification_des_poids():
    for i in range (0,n):
        ligne = MarketCaps.iloc[i]
        ligne = ligne.tolist()
        mois = ligne.pop(0)
        S = sum(ligne)
        print(mois,S)


taille_data = data.shape
n_2 = taille_data[0]
k_2 = taille_data[1]
dates = data.iloc[:,0]
dates = dates[1:]

def vérification_rendements():
    rendements = data.copy()
    for j in range (1,k_2):
        print("Le programme traite la colonne",j,"sur", k_2)
        colonne = data.iloc[:,j]
        colonne = colonne.tolist()
        colonne = colonne[1:]
        for i in range (3,n_2-1):
            if (colonne[i-1] == 0):
                rendements.iloc[i, j] = "erreur"
            elif (isinstance(colonne[i], float) and isinstance(colonne[i-1], float)):
                rendements.iloc[i,j] = colonne[i]/colonne[i-1] - 1
            else : 
                rendements.iloc[i, j] = "erreur"
    rendements.to_csv("rendements_test.csv", index=False)
                

#vérification_rendements()
#print(data.shape)
#print(type(type("bonjour")))
vérification_des_poids()
            
    