
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import Indicateurs_risque as Ir


def perf_moyenne_annualisée_secteurs(indices_boursiers_secteurs):
    dico_pmas = {}
    for i in range (1,10):
        indice_boursier = indices_boursiers_secteurs.iloc[:,[0,i]]
        sector_name = indices_boursiers_secteurs.columns[i]
        perf_moy_ann = Ir.perf_moyenne_annualisée(indice_boursier)
        dico_pmas[sector_name] = str(perf_moy_ann) + " %"
    return (dico_pmas)

def volatilité_annualisée_secteurs(indices_boursiers_secteurs):
    dico_vol = {}
    for i in range (1,10):
        indice_boursier = indices_boursiers_secteurs.iloc[:,[0,i]]
        sector_name = indices_boursiers_secteurs.columns[i]
        vol_ann = Ir.volatilité_annualisée(indice_boursier)
        dico_vol[sector_name] = str(vol_ann) + " %"
    return (dico_vol)
        
def volatilité_annualisée_secteurs_données_mensuelles(indices_boursiers_secteurs):
    dico_vol_mens = {}
    for i in range (1,10):
        indice_boursier = indices_boursiers_secteurs.iloc[:,[0,i]]
        sector_name = indices_boursiers_secteurs.columns[i]
        vol_ann_mens = Ir.volatilité_annualisée_données_mensuelles(indice_boursier)
        dico_vol_mens[sector_name] = str(vol_ann_mens) + " %"
    return (dico_vol_mens)

def calcule_drawdown_secteurs(indices_boursiers_secteurs):
    dico_drawdowns = {"Nom de secteur" : ("Max_drawdown", "Second_max_drawdown", "Max_drawdown en %", "Second_max_drawdown en %")}
    for i in range (1,10):
        indice_boursier = indices_boursiers_secteurs.iloc[:,[0,i]]
        sector_name = indices_boursiers_secteurs.columns[i]
        max_drawdown, second_max_drawdown, prop_max_drawdown, prop_second_max_drawdown = Ir.calcule_drawdown(indice_boursier)
        dico_drawdowns[sector_name] = (max_drawdown, second_max_drawdown, prop_max_drawdown, prop_second_max_drawdown)
    return (dico_drawdowns)

def calcule_VaR_secteurs(indices_boursiers_secteurs):
    dico_VaRs = {"Nom de secteur" : "VaR"}
    for i in range (1,10):
        indice_boursier = indices_boursiers_secteurs.iloc[:,[0,i]]
        sector_name = indices_boursiers_secteurs.columns[i]
        VaR = Ir.calcule_VaR(indice_boursier)
        dico_VaRs[sector_name] = VaR
    return (dico_VaRs)

def beta_secteurs(indices_boursiers_secteurs, indice_référence):
    if (len(indices_boursiers_secteurs) != len(indice_référence)):
        print("Erreur : les listes des deux indices ne sont pas du même format.")
        return ("Erreur")
    dico_betas = {"Nom de secteur" : "beta"}
    for i in range (1,10):
        indice_boursier = indices_boursiers_secteurs.iloc[:,i]
        indice_boursier = indice_boursier.values.tolist()
        indice_réf = indice_référence.iloc[:,1]
        #print(indice_réf)
        indice_réf = indice_réf.values.tolist()
        rendements_quotidiens = [(indice_boursier[j] - indice_boursier[j-1]) / indice_boursier[j-1] for j in range(1, len(indice_boursier))]
        rendements_réf = [(indice_réf[j] - indice_réf[j-1]) / indice_réf[j-1] for j in range(1, len(indice_réf))]
        sector_name = indices_boursiers_secteurs.columns[i]
        Cov_matrix = np.cov(rendements_quotidiens, rendements_réf)
        covariance = Cov_matrix[0,1]
        variance_ib_ref = Cov_matrix[1,1]
        dico_betas[sector_name] = covariance/variance_ib_ref
    return (dico_betas)

def tracking_error_secteurs_annualisée(indices_boursiers_secteurs, indice_référence):
    if (len(indices_boursiers_secteurs) != len(indice_référence)):
        print("Erreur : les listes des deux indices ne sont pas du même format.")
        return ("Erreur")
    dico_tracking_errors = {"Nom de secteur" : "Tracking error"}
    for i in range (1,10):
        indice_boursier = indices_boursiers_secteurs.iloc[:,i]
        indice_boursier = indice_boursier.values.tolist()
        indice_réf = indice_référence.iloc[:,1]
        indice_réf = indice_réf.values.tolist()
        rendements_quotidiens = [(indice_boursier[j] - indice_boursier[j-1]) / indice_boursier[j-1] for j in range(1, len(indice_boursier))]
        rendements_réf = [(indice_réf[j] - indice_réf[j-1]) / indice_réf[j-1] for j in range(1, len(indice_réf))]
        sector_name = indices_boursiers_secteurs.columns[i]
        n = int(len(rendements_quotidiens)/258)     # Nombre d'années. Une année comporte en moyenne 258 jours de bourse.
        lst_tracking_errors = []
        for j in range(n):
            rendements_quotidiens_j = rendements_quotidiens[len(rendements_quotidiens)-258*(j+1):len(rendements_quotidiens)-258*j]
            rendements_réf_j = rendements_réf[len(rendements_réf)-258*(j+1):len(rendements_réf)-258*j]
            S = 0
            for k in range (258):
                S = S + (rendements_quotidiens_j[k] - rendements_réf_j[k])**2
            tracking_error = np.sqrt(S/258)
            lst_tracking_errors.append(tracking_error)
        Tracking_error = sum(lst_tracking_errors)/n
        dico_tracking_errors[sector_name] = Tracking_error
    return (dico_tracking_errors)




path_1 = "C:/Users/Trist/Documents/Cours 2A - CS/Semestre 8/ST7 - Finance stochastique/Projet ST7/Indices boursiers par secteur/Indices_boursiers_par_secteur_1200j.csv"
#indices_boursiers_secteurs = pd.read_csv(path, sep=",",lineterminator='\n',skip_blank_lines=False, low_memory=False)
indices_boursiers_secteurs = pd.read_csv(path_1, sep=",", low_memory=False)
path_2 = "C:/Users/Trist/Documents/Cours 2A - CS/Semestre 8/ST7 - Finance stochastique/Projet ST7/Indice boursier global/Indice_boursier_1200j.csv"
indice_boursier_global = pd.read_csv(path_2, sep=",", low_memory=False)
#pmas = perf_moyenne_annualisée_secteurs(indices_boursiers_secteurs)
#print(pmas)
#vol_secteurs = volatilité_annualisée_secteurs(indices_boursiers_secteurs)
#print(vol_secteurs)
#vol_globale = Ir.volatilité_annualisée(indice_boursier_global)
#print("La volatilité annualisée de l'indice global est :", vol_globale)
#vol_secteurs_mens = volatilité_annualisée_secteurs_données_mensuelles(indices_boursiers_secteurs)
#print(vol_secteurs_mens)
#drawdowns_secteurs = calcule_drawdown_secteurs(indices_boursiers_secteurs)
#for cle, valeur in drawdowns_secteurs.items():
#    print(f'{cle}: {valeur}')
#drawdowns_ib_global = Ir.calcule_drawdown(indice_boursier_global)
#print("Les drawdowns maximaux pour l'indice boursier global sont quant à eux de :", drawdowns_ib_global)
#betas = beta_secteurs(indices_boursiers_secteurs, indice_boursier_global)
#for cle, valeur in betas.items():
#   print(f'{cle}: {valeur}')
tracking_errors = tracking_error_secteurs_annualisée(indices_boursiers_secteurs, indice_boursier_global)
for cle, valeur in tracking_errors.items():
    print(f'{cle}: {valeur}')