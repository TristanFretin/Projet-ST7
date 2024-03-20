
import numpy as np
import pandas as pd
import cvxpy as cvx
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

#path = "C:/Users/Trist/Documents/Cours 2A - CS/Semestre 8/ST7 - Finance stochastique/Projet ST7/Indice_boursier_1000j.csv"
#indice_boursier = pd.read_csv(path, sep=",",lineterminator='\n',skip_blank_lines=False, low_memory=False)

def perf_moyenne_annualisée(indice_boursier):
    n0 = indice_boursier.shape[0]
    n = int(n0/258)   # 258 est le nombre moyen de jours de bourse par an. Changer le 1000 si besoin !
    ib = indice_boursier.iloc[:,1]
    ib = ib.tolist()
    performances = []
    for i in range (n):
        rendements = []
        ib_i = ib[len(ib)-(i+1)*258:len(ib)-i*258]
        #print(len(ib_i))
        for j in range(257):
            rendement_i_j = ib_i[j+1]/ib_i[j]-1
            rendements.append(rendement_i_j)
        perf_moyenne_journalière = sum(rendements)/len(rendements)
        #perf = ib[-i*258-1]/ib[-(i+1)*258]
        performances.append(perf_moyenne_journalière*258)
    moyenne = sum(performances)/len(performances)
    perf_moy_ann = 100*moyenne
    #print("La performance moyenne annualisée est de ", perf_moy_ann,"%")
    return (perf_moy_ann)

def volatilité_annualisée(indice_boursier):
    n0 = indice_boursier.shape[0]
    n = int(n0/258)
    ib = indice_boursier.iloc[:,1]
    ib = ib.tolist()
    volatilités = []
    for i in range (n):
        ib_i = ib[-(i+1)*258:-i*258-1]
        rendements_quotidiens_i = [(ib_i[j] - ib_i[j-1]) / ib_i[j-1] for j in range(1, len(ib_i))]
        vol = np.std(rendements_quotidiens_i)
        volatilités.append(vol)
    moyenne = sum(volatilités)/len(volatilités)
    #print("La volatilité moyenne annualisée est de ", 100*moyenne,"%")
    return (100*moyenne)


def volatilité_annualisée_données_mensuelles(indice_boursier):
    n0 = indice_boursier.shape[0]
    n = int(n0/258)
    ib = indice_boursier.iloc[:,1]
    ib = ib.tolist()
    n_mois = int(n0/22)
    ib_mensuel = []
    for i in range (0,n_mois):      # prélèvement de données mensuelles uniquement.
        ib_mensuel.append(ib[i*22])
    volatilités = []
    for i in range (n):
        ib_mensuel_i = ib_mensuel[-(i+1)*12:-i*12-1]
        rendements_mensuels_i = [(ib_mensuel_i[j] - ib_mensuel_i[j-1]) / ib_mensuel_i[j-1] for j in range(1, len(ib_mensuel_i))]
        vol = np.std(rendements_mensuels_i)
        volatilités.append(vol)
    moyenne = sum(volatilités)/len(volatilités)
    #print("La volatilité moyenne annualisée avec des données mensuelles est de ", 100*moyenne,"%")
    return(100*moyenne)


def calcule_drawdown(indice_boursier):
    ib = indice_boursier.iloc[:,1]
    ib = ib.tolist()
    max_value = ib[0]
    drawdown = 0
    max_drawdown = 0
    prop_max_drawdown = 0
    second_max_drawdown = 0
    prop_second_max_drawdown = 0
    for value in ib:
        if value > max_value:
            max_value = value
        else:
            drawdown = max(drawdown, max_value - value)
            if (drawdown > max_drawdown):
                second_max_drawdown = max_drawdown
                prop_second_max_drawdown = prop_max_drawdown
                max_drawdown = drawdown
                prop_max_drawdown = max_drawdown/max_value
    #print("Le maximum drawdown de l'indice boursier est ", max_drawdown," soit, en pourcentage, un repli de ", 100*prop_max_drawdown,"%.")
    #print("Le deuxième maximum drawdown est ", second_max_drawdown, " soit, en pourcentage, un repli de ", 100*prop_second_max_drawdown, "%.")
    return (max_drawdown, second_max_drawdown, prop_max_drawdown*100, prop_second_max_drawdown*100)


def calcule_VaR(indice_boursier, confidence_level=0.95):
    ib = indice_boursier.iloc[:,1]
    ib = ib.tolist()
    gains_quotidiens = [(ib[j] - ib[j-1]) for j in range(1, len(ib))]
    sorted_gains = np.sort(gains_quotidiens)
    n = len(sorted_gains)
    percentile_index = int(n * (1 - confidence_level))
    var = sorted_gains[percentile_index]
    #print("La Value at Risk quotidienne avec un niveau de confiance de ", confidence_level, "%"," est de", var)
    return var


#path = "C:/Users/Trist/Documents/Cours 2A - CS/Semestre 8/ST7 - Finance stochastique/Projet ST7/Indices400j.csv"
#ibs = pd.read_csv(path, sep=",",lineterminator='\n',skip_blank_lines=False, low_memory=False)

#perf_moyenne_annualisée()
#volatilité_annualisée_données_mensuelles()
#calcule_drawdown()
#calcule_VaR(indice_boursier)
