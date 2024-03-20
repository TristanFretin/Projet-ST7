

import numpy as np
import pandas as pd
import cvxpy as cvx
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime


path = "C:/Users/Trist/Documents/Cours 2A - CS/Semestre 8/ST7 - Finance stochastique/Projet ST7/data_indexed.csv"
données = pd.read_csv(path, sep=",",lineterminator='\n',skip_blank_lines=False, low_memory=False)
path_2 = "C:/Users/Trist/Documents/Cours 2A - CS/Semestre 8/ST7 - Finance stochastique/Projet ST7/rendements_complets.csv"
rendements = pd.read_csv(path_2, sep=",",lineterminator='\n',skip_blank_lines=False, low_memory=False)

chemin_fichier_excel = "C:/Users/Trist/Documents/Cours 2A - CS/Semestre 8/ST7 - Finance stochastique/Projet ST7/DataProjets.xlsx"
xls = pd.ExcelFile(chemin_fichier_excel)
MarketCaps = pd.read_excel(xls, "MarketCaps")
taille = données.shape
n0 = taille[0]
#print(n0)
taille_2 = MarketCaps.shape
m0 = taille_2[0]
#print(m0)

def conversion_mois(string_mois_année):
    mois = string_mois_année[:3]
    année = string_mois_année[4:]
    date_chiffres = ""
    if (mois == "Jan"):
        mois_chiffre = "01"
    elif(mois == "Feb"):
        mois_chiffre = "02"
    elif(mois == "Mar"):
        mois_chiffre = "03"
    elif(mois == "Apr"):
        mois_chiffre = "04"
    elif(mois == "May"):
        mois_chiffre = "05"
    elif(mois == "Jun"):
        mois_chiffre = "06"
    elif(mois == "Jul"):
        mois_chiffre = "07"
    elif(mois == "Aug"):
        mois_chiffre = "08"
    elif(mois == "Sep"):
        mois_chiffre = "09"
    elif(mois == "Oct"):
        mois_chiffre = "10"
    elif(mois == "Nov"):
        mois_chiffre = "11"
    else:
        mois_chiffre = "12"
    date_chiffres = "20" + année + "-" + mois_chiffre
    return(date_chiffres)
        

def évolution_ib(n):
    ib = []
    init = n0-n
    mois_poids = MarketCaps.iloc[:,0].dt.month
    mois_poids = mois_poids.tolist()
    années_poids = MarketCaps.iloc[:,0].dt.year
    années_poids = années_poids.tolist()
    for i in range (n):
        valeurs = données.iloc[init+i,1:]        # Extraction des valeurs des actions à l'instant courant.
        valeurs = valeurs.tolist()
        valeurs = list(map(float, valeurs))     # On convertit les chaînes de caractères en flottants.
        date = données.iloc[init+i,0]
        date_tronquée = date[:-3]       # On enlève le jour, qui car nous avons juste besoin de connaître le mois pour savoir quelles sont les poids des différentes entreprises.
        j = 1
        mois = str(mois_poids[j])
        année = str(années_poids[j])
        année_mois = année + "-" + mois
        #date2 = conversion_mois(mois)
        while (j<m0-1 and année_mois != date_tronquée):
            j=j+1
            mois = str(mois_poids[j])
            année = str(années_poids[j])
            année_mois = année + "-" + mois 
            #date2 = conversion_mois(mois)
        if (j==m0):
            print("Erreur")
            return("erreur")
        else:
            poids = MarketCaps.iloc[j,1:]
            poids = poids.tolist()
            ib_i = 0
            for k in range (0,len(poids)):
                if np.isnan(valeurs[k]):
                    pass
                else:
                    ib_i = ib_i + poids[k]*valeurs[k]
            ib.append(ib_i)
    #print(ib)
    plt.plot(ib)
    plt.xlabel('Temps')
    plt.ylabel('S&P 300')
    title = "Valeurs du S&P 300 sur les " + str(n) + " derniers jours d'ouverture de la bourse."
    plt.title(title)
    plt.show()
            


def évolution_ib_rendements(n):
    ibr = [1]
    init = n0-n-1
    mois_poids = MarketCaps.iloc[:,0].dt.month
    mois_poids = mois_poids.tolist()
    années_poids = MarketCaps.iloc[:,0].dt.year
    années_poids = années_poids.tolist()
    dates = [rendements.iloc[init,0]]
    for i in range (1,n):
        valeurs = rendements.iloc[init+i,1:]        # Extraction des valeurs des actions à l'instant courant.
        valeurs = valeurs.replace('erreur', '0')
        valeurs = valeurs.replace('erreur\r\r', '0')
        valeurs = valeurs.tolist()
        valeurs = list(map(float, valeurs))     # On convertit les chaînes de caractères en flottants.
        date = rendements.iloc[init+i,0]
        date_tronquée = date[:-3]       # On enlève le jour, qui car nous avons juste besoin de connaître le mois pour savoir quelles sont les poids des différentes entreprises.
        j = 1
        mois = str(mois_poids[j])
        année = str(années_poids[j])
        année_mois = année + "-" + mois
        dates.append(date)
        #date2 = conversion_mois(mois)
        while (j<m0-1 and année_mois != date_tronquée):
            j=j+1
            mois = str(mois_poids[j])
            année = str(années_poids[j])
            année_mois = année + "-" + mois 
            #date2 = conversion_mois(mois)
        if (j==m0):
            print("Erreur")
            return("erreur")
        else:
            poids = MarketCaps.iloc[j,1:]
            poids = poids.tolist()
            taux = 0        # Taux de croissance de notre indice par rapport à la veille.
            for k in range (0,len(poids)):
                if np.isnan(valeurs[k]):        # On enlève les valeurs Nan pour ne pas polluer notre indice.
                    pass
                else:
                    taux = taux + poids[k]*valeurs[k]
            ibr.append(ibr[-1]*(1 + taux))
    #print(ibr)
    liste_dates = [datetime.strptime(date_str, '%Y-%m-%d') for date_str in dates]    # Mise des dates au format datetime.
    df = pd.DataFrame({'ibr': ibr}, index=liste_dates)
    name_file = "Indice_boursier_"+str(n)+"j.csv"
    df.to_csv(name_file, index=True)
    plt.figure(figsize=(12, 7))
    plt.plot(df.index, df['ibr'], marker='o', markersize=1, linestyle='-')  # Tracer la courbe
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))  # Format AAAA-MM-JJ
    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=122))  # Afficher une date tous les 10 jours
    plt.xticks(rotation=45)
    plt.xlabel('Temps')
    plt.ylabel('Notre indice boursier')
    plt.grid(True)
    title = "Valeurs de notre indice de rendement sur les " + str(n) + " derniers jours d'ouverture de la bourse."
    plt.title(title)
    plt.tight_layout()
    plt.show()      



#print(conversion_mois("Mar-02"))   
évolution_ib_rendements(1200)


