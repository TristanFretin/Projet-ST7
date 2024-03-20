import pandas as pd
import yaml


# Load config file
with open("config.yaml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)


prices_path = cfg["Prices_path"]
prices = pd.read_csv(prices_path, index_col=0)

# Calculer les rendements
return_path = cfg["returns_path"]
returns = prices.pct_change()
returns.to_csv(return_path, index=True)    # Sauvegarde en CSV sans les index

# Print the dimensions of the data
print("Les dimensions des rendements sont: ", returns.shape)
