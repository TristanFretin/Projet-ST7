
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import 


path_1 = "C:/Users/Trist/Documents/Cours 2A - CS/Semestre 8/ST7 - Finance stochastique/Projet ST7/rendements_complets.csv"
rendements = pd.read_csv(path_1, sep=",",lineterminator='\n',skip_blank_lines=False, low_memory=False)

chemin_fichier_excel = "C:/Users/Trist/Documents/Cours 2A - CS/Semestre 8/ST7 - Finance stochastique/Projet ST7/DataProjets.xlsx"
xls = pd.ExcelFile(chemin_fichier_excel)
MarketCaps = pd.read_excel(xls, "MarketCaps")
Mapping = pd.read_excel(xls, "Mapping")
Sectors = pd.read_excel(xls, "Sector")

Mapping_sectors = Mapping.iloc[1:10,3:5]
taille = rendements.shape
n0 = taille[0]
taille_2 = MarketCaps.shape
m0 = taille_2[0]

def rendements_secteurs(n):
    ibr = [[1,1,1,1,1,1,1,1,1]]
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
            #print("La somme des poids vaut ", sum(poids), "le ", date)
            secteurs = Sectors.iloc[j,1:]
            secteurs = secteurs.tolist()
            ibr_i = []
            poids_total = 0
            for l in range (0,9):
                sector_id = Mapping_sectors.iloc[l,0]
                sector_name = Mapping_sectors.iloc[l,1]
                poids_secteur = 0
                taux = 0        # Taux de croissance de notre indice par rapport à la veille.
                for k in range (0,len(poids)):
                    if np.isnan(valeurs[k]):        # On enlève les valeurs Nan pour ne pas polluer notre indice.
                        pass
                    else:
                        if (secteurs[k] == sector_id):
                            taux = taux + poids[k]*valeurs[k]
                            poids_secteur = poids_secteur + poids[k]
                if (poids_secteur == 0):
                    print("Le poids du secteur ", sector_id, "est nul pour le mois ", année_mois)
                    print(poids_secteur)
                    taux = 0
                else:
                    taux = taux/poids_secteur
                    #if (taux<-1):
                        #print("La performance du secteur ", sector_id, "est inférieure à -100%", "le ", date )
                ibr_i.append(ibr[len(ibr)-1][l]*(1 + taux))
                poids_total = poids_total + poids_secteur
            ibr.append(ibr_i)
            #print("Le poids total reconstitué est de ", poids_total, "le ", date)
    #print(ibr)
    liste_dates = [datetime.strptime(date_str, '%Y-%m-%d') for date_str in dates]    # Mise des dates au format datetime.
    noms_colonnes = Mapping_sectors.iloc[:,1]
    noms_colonnes = noms_colonnes.tolist()
    df = pd.DataFrame(ibr, index=liste_dates, columns=noms_colonnes)
    name_file = "Indices_boursiers_par_secteur_"+str(n)+"j.csv"
    df.to_csv(name_file, index=True)
    plt.figure(figsize=(12, 7))
    for colonne in df.columns:
        plt.plot(df.index, df[colonne], marker='o', markersize=1, linestyle='-', label=colonne)  # Tracer la courbe
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))  # Format AAAA-MM-JJ
    intervalle = int(n/10)      # On impose qu'il y ait 10 graduations de dates.
    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=intervalle))  # Afficher une date tous les 10 jours
    plt.xticks(rotation=45)
    plt.xlabel('Temps')
    plt.ylabel('Notre indice boursier')
    plt.grid(True)
    title = "Valeurs des indices de rendement par secteur sur les " + str(n) + " derniers jours d'ouverture de la bourse."
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.show()      






#rendements_secteurs(400)