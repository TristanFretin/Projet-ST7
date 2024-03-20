
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import Indicateurs_risque as Ir
import time
import math
import Markowitz as Mk
            

def ib_EW(rendements, n):
    taille = rendements.shape
    n0 = taille[0]
    ibr = [1]
    init = n0-n-1
    dates = rendements.iloc[init:n0-1,0]
    dates = dates.values.tolist()
    for i in range (1,n):
        valeurs = rendements.iloc[init+i,1:]        # Extraction des valeurs des actions à l'instant courant.
        valeurs = valeurs.replace('erreur', '0')
        valeurs = valeurs.replace('erreur\r\r', '0')
        valeurs = valeurs.tolist()
        valeurs = list(map(float, valeurs))     # On convertit les chaînes de caractères en flottants.
        date = rendements.iloc[init+i,0]
        taux = 0        # Taux de croissance de notre indice par rapport à la veille.
        N = 0       # Nombre d'entreprises dans l'indice.
        for k in range (0,len(valeurs)):
            if np.isnan(valeurs[k]):        # On enlève les valeurs Nan pour ne pas polluer notre indice.
                pass
            else:
                N = N + 1
                taux = taux + valeurs[k]
        taux = taux/N
        ibr.append(ibr[-1]*(1 + taux))
    #dates_string = [serie.astype(str) for serie in dates]
    #dates_string = [str(serie) for serie in dates]
    #print(dates_string)
    liste_dates = [datetime.strptime(date_str, '%Y-%m-%d') for date_str in dates]    # Mise des dates au format datetime.
    df = pd.DataFrame({'ibr': ibr}, index=liste_dates)
    name_file = "Indice_boursier_"+str(n)+"j.csv"
    #df.to_csv(name_file, index=True)
    plt.figure(figsize=(12, 7))
    plt.plot(df.index, df['ibr'], marker='o', markersize=1, linestyle='-')  # Tracer la courbe
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))  # Format AAAA-MM-JJ
    intervalle = int(n/10)
    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=intervalle))  # Afficher une date tous les 10 jours
    plt.xticks(rotation=45)
    plt.xlabel('Temps')
    plt.ylabel('Notre indice boursier')
    plt.grid(True)
    title = "Valeurs de notre indice EW de rendement sur les " + str(n) + " derniers jours d'ouverture de la bourse."
    plt.title(title)
    plt.tight_layout()
    plt.show()      


# Cette fonction calcule les poids pour les stratégies ERB et IV.
def inv_volatilités_entreprises(rendements, init, mode='ERB', nombre_mois_retour=1): 
    taille = rendements.shape
    n0 = taille[0]
    m0 = taille[1]
    poids = []
    mois = []
    dates = rendements.iloc[init:,0]
    dates = dates.tolist()
    
    # Dans cette partie de la fonction, on collecte les positions des premiers jours boursiers de chaque mois.
    t = 0
    pos_début_mois = [0]
    dates_début_mois = [dates[0]]
    while (t<n0-init-1):
        t0 = t
        mois = dates[t0][:-3]
        while (t<n0-init-1 and mois == dates[t][:-3]):
            t = t+1
        pos_début_mois.append(t)
        dates_début_mois.append(dates[t])
    #print(dates_début_mois)
        
    # Dans cette partie de la fonction, on calcule les volatilités mensuelles des entreprises.        
    for j in range (1,m0):
        print("Traitement de l'entreprise", j, "sur", m0, end='\r')
        rendements_entreprise = rendements.iloc[init:,j]
        rendements_entreprise = rendements_entreprise.tolist()
        poids_entreprise = []
        for i in range (len(pos_début_mois)-nombre_mois_retour-1):
            rendements_entreprise_mois = rendements_entreprise[pos_début_mois[i]:pos_début_mois[i+nombre_mois_retour]]
            rendements_entreprise_mois = [float(rendement) if (rendement != "erreur" and rendement!= "erreur\r\r") else 0 for rendement in rendements_entreprise_mois]
            #print(rendements_entreprise_mois)
            vol = np.std(rendements_entreprise_mois)
            #print("La volatilité de l'entreprise", j, "sur le mois", i, "est de", vol)
            if (mode == 'ERB'):
                poids_entreprise.append(1/vol)
            elif (mode == 'IV') :
                poids_entreprise.append(1/vol**2)
            else :
                print("Erreur : l'argument mode est incorrect. Il doit être égal à 'ERB' ou 'IV'.")
        poids.append(poids_entreprise)
    
    #Dernier bout de la fonction :)
    poids_np = np.array(poids)
    poids_np = np.transpose(poids_np)
    poids_df = pd.DataFrame(poids_np)
    poids_df.index = dates_début_mois[nombre_mois_retour:-1]
    #print(poids_df)
    return(poids_df)
        

## On écrit ici une fonction qui nous servira dans la fonction pondérations_MV. Cette fonction prend en argument un tableau symétrique
## Numpy, et renvoie ce même tableau privé de se colonnes et lignes nulles, ainsi qu'une liste contenant les numéros des colonnes supprimées.

def enlever_colonnes_nulles(tableau):
    numéros_colonnes_nulles = []    # Cette liste stockera les numéros des colonnes nulles.
    for i in range(tableau.shape[1]):
        if (np.sum(np.abs(tableau[:, i])) == 0): # Si la norme 1 de la colonne est nulle, alors la colonne est nulle.
            numéros_colonnes_nulles.append(i)
    tableau_sans_colonnes_nulles = np.delete(tableau, numéros_colonnes_nulles, axis=1)  # On supprime les colonnes nulles.
    tableau_sans_colonnes_ni_lignes_nulles = np.delete(tableau_sans_colonnes_nulles, numéros_colonnes_nulles, axis=0)  # On supprime aussi les lignes correspondantes (la matrice initiale est symétrique).
    return (tableau_sans_colonnes_ni_lignes_nulles, numéros_colonnes_nulles)



def pondérations_MV(rendements, init, nombre_mois_retour=1):
    taille = rendements.shape
    n0 = taille[0]
    m0 = taille[1]
    poids = []
    mois = []
    dates = rendements.iloc[init:,0]
    dates = dates.tolist()
    
    # Dans cette partie de la fonction, on collecte les positions des premiers jours boursiers de chaque mois.
    t = 0
    pos_début_mois = [0]
    dates_début_mois = [dates[0]]
    while (t<n0-init-1):
        t0 = t
        mois = dates[t0][:-3]
        while (t<n0-init-1 and mois == dates[t][:-3]):
            t = t+1
        pos_début_mois.append(t)
        dates_début_mois.append(dates[t])
    
    for i in range (len(pos_début_mois)-nombre_mois_retour-1):
        poids_i = []
        rendements_mois = rendements.iloc[pos_début_mois[i]+init:pos_début_mois[i+nombre_mois_retour]+init,1:]
        rendements_mois = rendements_mois.values
        rendements_mois[rendements_mois == "erreur"]=0
        rendements_mois[rendements_mois == "erreur\r\r"]=0
        rendements_mois[rendements_mois == "\r\r\r"]=0
        #print("rendements_mois au mois", i, ":\n", rendements_mois)
        rendements_mois_float = rendements_mois.astype(float)
        rendements_mois_float[np.isnan(rendements_mois_float)]=0
        #print("Matrice des rendements au mois", i, ":\n", rendements_mois_float)
        #print(rendements_mois_float.shape)
        rendements_mois_float = np.transpose(rendements_mois_float)
        #rendements_mois_float_nettoyée, lst_colonnes_nulles = enlever_colonnes_nulles(rendements_mois_float)
        #rendements_entreprise_mois = [float(rendement) if (rendement != "erreur" and rendement!= "erreur\r\r") else 0 for rendement in rendements_entreprise_mois]
        #print(rendements_entreprise_mois)
        matrice_covariance_i = np.cov(rendements_mois_float)
        matrice_covariance_i_nettoyée, lst_colonnes_nulles = enlever_colonnes_nulles(matrice_covariance_i)
        #print("Matrice de covariance nettoyée du mois", i, ":\n", matrice_covariance_i_nettoyée)
        taille_mcin = matrice_covariance_i_nettoyée.shape
        #print(taille_mcin)
        matrice_covariance_i_inverse = np.linalg.inv(matrice_covariance_i_nettoyée)
        #print(matrice_covariance_i_inverse)
        #print("La matrice de covariance du mois", i, "est de taille :", matrice_covariance_i_inverse.shape)
        c_1 = 0     # Compteur de l'ensemble des poids.
        c_2 = 0     # Compteur du nombre de poids nuls rajoutés.
        for j in range(1,taille_mcin[0]):
            c_1 = j+c_2
            while (c_1 in lst_colonnes_nulles):
                poids_i.append(0)
                c_2 = c_2+1
                c_1 = c_1+1
            inv_covariances_j = matrice_covariance_i_inverse[j-1,:]
            poids_i_j = sum(inv_covariances_j)
            poids_i.append(abs(poids_i_j))      # Pas de short, donc on impose que les poids soient positifs.
        poids.append(poids_i)
        #print("Longueur de la liste de poids :", len(poids_i))
    #poids_np = np.array(poids)
    poids_df = pd.DataFrame(poids)
    poids_df.index = dates_début_mois[nombre_mois_retour:-1]
    #print(poids_df)
    return(poids_df)
    

# Cette fonction va calculer les poids du portefeuille de Markovitz, qui maximise la prévision de gain pour un risque donné. La prévision de gain est calculée en se basant sur les moyennes des gains des mois précédents.

def pondérations_Mk(rendements, init, nombre_mois_retour=1, risk_constraint=0.01):
    taille = rendements.shape
    n0 = taille[0]
    m0 = taille[1]
    poids = []
    mois = []
    dates = rendements.iloc[init:,0]
    dates = dates.tolist()
    
    # Dans cette partie de la fonction, on collecte les positions des premiers jours boursiers de chaque mois.
    t = 0
    pos_début_mois = [0]
    dates_début_mois = [dates[0]]
    while (t<n0-init-1):
        t0 = t
        mois = dates[t0][:-3]
        while (t<n0-init-1 and mois == dates[t][:-3]):
            t = t+1
        pos_début_mois.append(t)
        dates_début_mois.append(dates[t])
    
    for i in range (len(pos_début_mois)-nombre_mois_retour-1):
        rendements_mois = rendements.iloc[pos_début_mois[i]+init:pos_début_mois[i+nombre_mois_retour]+init,1:]
        rendements_mois = rendements_mois.values
        rendements_mois[rendements_mois == "erreur"]=0
        rendements_mois[rendements_mois == "erreur\r\r"]=0
        rendements_mois[rendements_mois == "\r\r\r"]=0
        #print("rendements_mois au mois", i, ":\n", rendements_mois)
        rendements_mois_float = rendements_mois.astype(float)
        rendements_mois_float[np.isnan(rendements_mois_float)]=0
        #print("Matrice des rendements au mois", i, ":\n", rendements_mois_float)
        #print(rendements_mois_float.shape)
        rendements_mois_float = np.transpose(rendements_mois_float)
        #rendements_mois_float_nettoyée, lst_colonnes_nulles = enlever_colonnes_nulles(rendements_mois_float)
        #rendements_entreprise_mois = [float(rendement) if (rendement != "erreur" and rendement!= "erreur\r\r") else 0 for rendement in rendements_entreprise_mois]
        #print(rendements_entreprise_mois)
        gain_prévisionnel_i = np.mean(rendements_mois_float, axis=1)    # On calcule la moyenne des rendements des entreprises sur les derniers mois.
        matrice_covariance_i = np.cov(rendements_mois_float)    # On calcule la matrice de covariance des entreprises sur les derniers mois.
        #print("Les rendements moyens à l'étape", i, "sont : \n", gain_prévisionnel_i)
        w_MVO_i = Mk.opti_base(gain_prévisionnel_i, matrice_covariance_i, risk_constraint=risk_constraint)  # La contrainte de risque étant fixée, on détermine les poids qui auraient maximisé les gains sur les derniers mois.
        poids.append(w_MVO_i)
        #print("Longueur de la liste de poids :", len(poids_i))
    #poids_np = np.array(poids)
    poids_df = pd.DataFrame(poids)
    poids_df.index = dates_début_mois[nombre_mois_retour:-1]
    #print(poids_df)
    return(poids_df)
    


def ib_ERB(rendements, n):      # Pour cet indice, le poids d'une entreprise au mois i est proportionnel à l'inverse de sa volatilité sur le mois i-1.
    taille = rendements.shape
    n0 = taille[0]
    ibr = [1]
    init = n0-n-1
    poids = inv_volatilités_entreprises(rendements, init-30)    # On commence à calculer les volatilités un mois plus tôt car les poids d'un mois sont déterminés grâce aux volatilités du mois précédent.
    dates_début_mois = poids.index
    dates = rendements.iloc[init:n0-1,0]
    dates = dates.tolist()
    for i in range (1,n):
        valeurs = rendements.iloc[init+i,1:]        # Extraction des rendements des actions à l'instant courant.
        valeurs = valeurs.replace('erreur', '0')
        valeurs = valeurs.replace('erreur\r\r', '0')
        valeurs = valeurs.tolist()
        valeurs = list(map(float, valeurs))     # On convertit les chaînes de caractères en flottants.
        date = rendements.iloc[init+i,0]
        date_tronquée = date[:-3]       # On enlève le jour, qui car nous avons juste besoin de connaître le mois pour savoir quelles sont les poids des différentes entreprises.
        j = 0
        date_début_mois = dates_début_mois[j]
        mois = date_début_mois[:-3]
        #dates.append(date)
        while (j<len(dates_début_mois)-1 and mois != date_tronquée):
            j=j+1
            date_début_mois = dates_début_mois[j]
            mois = date_début_mois[:-3]
        if (j==len(dates_début_mois)):
            print("Erreur")
            return("erreur")
        else:
            poids_i = poids.iloc[j,1:]
            poids_i = poids_i.tolist()
            taux = 0        # Taux de croissance de notre indice par rapport à la veille.
            somme_poids = 0
            for k in range (0,len(poids_i)):
                if np.isnan(valeurs[k]):        # On enlève les valeurs Nan pour ne pas polluer notre indice.
                    pass
                elif math.isinf(poids_i[k]) or np.isnan(poids_i[k]):
                    pass
                else:
                    taux = taux + poids_i[k]*valeurs[k]
                    somme_poids = somme_poids + poids_i[k]
            ibr.append(ibr[-1]*(1 + taux/somme_poids))
    print(ibr)
    liste_dates = [datetime.strptime(date_str, '%Y-%m-%d') for date_str in dates]    # Mise des dates au format datetime.
    df = pd.DataFrame({'ibr': ibr}, index=liste_dates)
    name_file = "Indice_boursier_"+str(n)+"j.csv"
    #df.to_csv(name_file, index=True)
    plt.figure(figsize=(12, 7))
    plt.plot(df.index, df['ibr'], marker='o', markersize=1, linestyle='-')  # Tracer la courbe
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))  # Format AAAA-MM-JJ
    intervalle = int(n/10)
    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=intervalle))  # Afficher une date tous les 10 jours
    plt.xticks(rotation=45)
    plt.xlabel('Temps')
    plt.ylabel('Notre indice boursier')
    plt.grid(True)
    title = "Valeurs de l'indice ERB de rendement sur les " + str(n) + " derniers jours d'ouverture de la bourse."
    plt.title(title)
    plt.tight_layout()
    plt.show()      



def ibs_réf(rendements, n, supervision='no', nombre_mois_retour=1, Mk_risk_constraint=0.01):      # Cette fonction va tracer les différents indices boursiers de référence : EW, ERB, IV.
    chemin_fichier_excel = "C:/Users/Trist/Documents/Cours 2A - CS/Semestre 8/ST7 - Finance stochastique/Projet ST7/DataProjets.xlsx"
    xls = pd.ExcelFile(chemin_fichier_excel)
    MarketCaps = pd.read_excel(xls, "MarketCaps")
    taille = rendements.shape
    n0 = taille[0]
    ib_EW = [1]
    ib_ERB = [1]
    ib_IV = [1]
    ib_MV = [1]
    ib_Mk = [1]
    init = n0-n-1
    poids_ERB = inv_volatilités_entreprises(rendements, init-21*(nombre_mois_retour+1), mode='ERB', nombre_mois_retour=nombre_mois_retour)    # On commence à calculer les volatilités nombre_mois_retour mois plus tôt car les poids d'un mois sont déterminés grâce aux volatilités des nombre_mois_retour mois précédents.
    poids_IV = inv_volatilités_entreprises(rendements, init-21*(nombre_mois_retour+1), mode='IV', nombre_mois_retour=nombre_mois_retour)
    poids_MV = pondérations_MV(rendements, init-21*(nombre_mois_retour+1), nombre_mois_retour=nombre_mois_retour)
    poids_Mk = pondérations_Mk(rendements, init-21*(nombre_mois_retour+1), nombre_mois_retour=nombre_mois_retour, risk_constraint=Mk_risk_constraint**2)
    #print("Les poids de Markowitz sont : \n", poids_Mk)
    dates_début_mois = poids_ERB.index
    dates = rendements.iloc[init:n0-1,0]
    dates = dates.tolist()
    for i in range (1,n):
        valeurs = rendements.iloc[init+i,1:]        # Extraction des rendements des actions à l'instant courant.
        valeurs = valeurs.replace('erreur', '0')
        valeurs = valeurs.replace('erreur\r\r', '0')
        valeurs = valeurs.tolist()
        valeurs = list(map(float, valeurs))     # On convertit les chaînes de caractères en flottants.
        date = rendements.iloc[init+i,0]
        date_tronquée = date[:-3]       # On enlève le jour, qui car nous avons juste besoin de connaître le mois pour savoir quelles sont les poids des différentes entreprises.
        j = 0
        date_début_mois = dates_début_mois[j]
        mois = date_début_mois[:-3]
        #dates.append(date)
        while (j<len(dates_début_mois)-1 and mois != date_tronquée):
            j=j+1
            date_début_mois = dates_début_mois[j]
            mois = date_début_mois[:-3]
        if (j==len(dates_début_mois)):
            print("Erreur")
            return("erreur")
        else:
            MarketCaps_i = MarketCaps.iloc[j,1:]
            MarketCaps_i = MarketCaps_i.tolist()
            #print(len(MarketCaps_i))
            poids_ERB_i = poids_ERB.iloc[j,1:]
            poids_ERB_i = poids_ERB_i.tolist()
            #print("Longueur de la liste des poids ERB :",len(poids_ERB_i))
            poids_IV_i = poids_IV.iloc[j,1:]
            poids_IV_i = poids_IV_i.tolist()
            poids_MV_i = poids_MV.iloc[j,0:]
            poids_MV_i = poids_MV_i.tolist()
            poids_Mk_i = poids_Mk.iloc[j,0:]
            poids_Mk_i = poids_Mk_i.tolist()
            #print(len(poids_MV_i))
            #print(len(poids_Mk_i))
            #print("Poids MV au jour", i, ":",poids_MV_i)
            taux_EW = 0
            taux_ERB = 0        # Taux de croissance de notre indice par rapport à la veille.
            taux_IV = 0
            taux_MV = 0
            taux_Mk = 0
            somme_poids_EW = 0
            somme_poids_ERB = 0
            somme_poids_IV = 0
            somme_poids_MV = 0
            somme_poids_Mk = 0
            for k in range (0,len(poids_ERB_i)):
                if np.isnan(valeurs[k]):        # On enlève les valeurs Nan pour ne pas polluer notre indice.
                    pass
                elif (MarketCaps_i[k]==0 and supervision=='yes'):
                    pass
                else: 
                    taux_EW = taux_EW + valeurs[k]
                    somme_poids_EW = somme_poids_EW + 1
                    if math.isinf(poids_ERB_i[k]) or np.isnan(poids_ERB_i[k]):
                        pass
                    else:
                        taux_ERB = taux_ERB + poids_ERB_i[k]*valeurs[k]
                        somme_poids_ERB = somme_poids_ERB + poids_ERB_i[k]
                    if math.isinf(poids_IV_i[k]) or np.isnan(poids_IV_i[k]):
                        pass
                    else:
                        taux_IV = taux_IV + poids_IV_i[k]*valeurs[k]
                        somme_poids_IV = somme_poids_IV + poids_IV_i[k]
                    if math.isinf(poids_MV_i[k]) or np.isnan(poids_MV_i[k]):
                        pass
                    else:
                        taux_MV = taux_MV + poids_MV_i[k]*valeurs[k]
                        somme_poids_MV = somme_poids_MV + poids_MV_i[k]
                    if math.isinf(poids_Mk_i[k]) or np.isnan(poids_Mk_i[k]):
                        pass
                    else:
                        taux_Mk = taux_Mk + poids_Mk_i[k]*valeurs[k]
                        somme_poids_Mk = somme_poids_Mk + poids_Mk_i[k]
            ib_EW.append(ib_EW[-1]*(1 + taux_EW/somme_poids_EW))
            ib_ERB.append(ib_ERB[-1]*(1 + taux_ERB/somme_poids_ERB))
            ib_IV.append(ib_IV[-1]*(1 + taux_IV/somme_poids_IV))
            ib_MV.append(ib_MV[-1]*(1 + taux_MV/somme_poids_MV))
            ib_Mk.append(ib_Mk[-1]*(1 + taux_Mk/somme_poids_Mk)) 
    #print("ib_EW", ib_EW)
    #print("ib_ERB", ib_ERB)
    #print("ib_IV", ib_IV)
    liste_dates = [datetime.strptime(date_str, '%Y-%m-%d') for date_str in dates]    # Mise des dates au format datetime.
    #df_EW = pd.DataFrame({'ib_EW': ib_EW}, index=liste_dates)
    #df_ERB = pd.DataFrame({'ib_ERB': ib_ERB}, index=liste_dates)
    #df_IV = pd.DataFrame({'ib_IV': ib_IV}, index=liste_dates)
    #df = pd.DataFrame({'ib_EW': ib_EW, 'ib_ERB': ib_ERB, 'ib_IV': ib_IV}, index=liste_dates)
    df = pd.DataFrame({'ib_EW': ib_EW, 'ib_ERB': ib_ERB, 'ib_IV': ib_IV, 'ib_MV': ib_MV, 'ib_Mk': ib_Mk}, index=liste_dates)
    name_file = "Indices_"+str(n)+"j.csv"
    df.to_csv(name_file, index=True)
    plt.figure(figsize=(12, 7))
    plt.plot(df.index, df['ib_EW'], marker='o', markersize=1, linestyle='-', label = "Ib_EW")  # Tracer la courbe
    plt.plot(df.index, df['ib_ERB'], marker='o', markersize=1, linestyle='-', label="Ib_ERB")
    plt.plot(df.index, df['ib_IV'], marker='o', markersize=1, linestyle='-', label="Ib_IV")
    plt.plot(df.index, df['ib_MV'], marker='o', markersize=1, linestyle='-', label="Ib_MV")
    Mk_label = "Ib_Mk avec risque = " + str(Mk_risk_constraint)
    plt.plot(df.index, df['ib_Mk'], marker='o', markersize=1, linestyle='-', label=Mk_label)
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))  # Format AAAA-MM-JJ
    intervalle = int(n/10)
    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=intervalle))  # Afficher une date tous les 10 jours
    plt.xticks(rotation=45)
    plt.xlabel('Temps')
    plt.ylabel("Valeur de l'indice boursier, relativement à la valeur initiale")
    plt.grid(True)
    title = "Valeurs des indices de rendement sur les " + str(n) + " derniers jours d'ouverture de la bourse."
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.show()      


def comparaisons_ibs(ibs):
    dico_indicateurs = {"Nom de l'indice": ("perf_moy_ann", "vol_ann", "vol_ann_mens", "max_drawdown", "second_max_drawdown", "prop_max_drawdown", "prop_second_max_drawdown", "VaR")}
    names_ib = ["ib_EW", "ib_ERB", "ib_IV", "ib_MV", "ib_Mk"]
    for i in range (1,6):
        ib = ibs.iloc[:,[0,i]]
        perf_moy = Ir.perf_moyenne_annualisée(ib)
        vol = Ir.volatilité_annualisée(ib)
        vol_mens = Ir.volatilité_annualisée_données_mensuelles(ib)
        max_drawdown, second_max_drawdown, prop_max_drawdown, prop_second_max_drawdown = Ir.calcule_drawdown(ib)
        VaR = Ir.calcule_VaR(ib)
        dico_indicateurs[names_ib[i-1]] = (perf_moy, vol, vol_mens, max_drawdown, second_max_drawdown, prop_max_drawdown, prop_second_max_drawdown, VaR)
    print("Dictionnaire des indicateurs pour les différents indices :")
    for cle, valeur in dico_indicateurs.items():
        print(cle, ":", valeur)
    print("Terminé.")
        



path = "C:/Users/Trist/Documents/Cours 2A - CS/Semestre 8/ST7 - Finance stochastique/Projet ST7/rendements_réduits.csv"
rendements = pd.read_csv(path, sep=",",lineterminator='\n',skip_blank_lines=False, low_memory=False)

#ib_EW(rendements, 400)
#temps_début = time.time()
#ibs_réf(rendements, 400, supervision='yes', nombre_mois_retour=6, Mk_risk_constraint=0.05)
#temps_fin = time.time()
#temps_exécution = temps_fin - temps_début
#print("Temps d'exécution :", temps_exécution, "secondes")


path_ib = "C:/Users/Trist/Documents/Cours 2A - CS/Semestre 8/ST7 - Finance stochastique/Projet ST7/Indices_400j.csv"
ibs = pd.read_csv(path_ib, sep=",",lineterminator='\n',skip_blank_lines=False, low_memory=False)

comparaisons_ibs(ibs)



