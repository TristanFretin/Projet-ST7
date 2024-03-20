
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time
import math
import cvxpy as cp
import random


Names = ["Equity USA", "Equity EMU", "Bond EUR Sovereign", "Bond EUR IG Corp", "Cash"]
mu = np.array([0.057, 0.066, 0.033, 0.016, 0.002])
sigma = [0.143, 0.164, 0.083, 0.04, 0.005]
rho = np.array([[1, 0.821, -0.05, 0.25, 0],
       [0.821, 1, -0.14, 0.1, 0],
       [-0.05, -0.14, 1, 0.67, 0],
       [0.25, 0.1, 0.67, 1, 0],
       [0, 0, 0, 0, 1]])

Cov_matrice = np.diag(sigma) @ rho @ np.diag(sigma)


def opti_base(mu, Cov_matrice, risk_constraint=0.01):
       # Créer une variable pour l'indice de l'élément maximal.
       taille = mu.shape
       print(taille)
       m = taille[0]
       w = cp.Variable(m)
       # Contrainte pour s'assurer que w est valide.
       constraints = [cp.sum(w) == 1, cp.quad_form(w, Cov_matrice) <= risk_constraint, w>=0]
       # Définir l'objectif pour maximiser l'élément correspondant à l'indice i
       objective = cp.Maximize(mu @ w)
       # Définir le problème d'optimisation
       problem = cp.Problem(objective, constraints)
       # Résoudre le problème
       problem.solve()
       # L'indice de l'élément maximal
       w_MVO = w.value
       print("Le vecteur w_MVO qui maximise le gain est :", w_MVO)
       return(w_MVO)
       
def opti_lagrangien():
       # Créer une variable pour l'indice de l'élément maximal
       w = cp.Variable(5)
       # Contrainte pour s'assurer que w est valide
       constraints = [cp.sum(w) == 1, cp.quad_form(w, Cov_matrice) <= 0.01, w>=0]
       # Définir l'objectif pour maximiser l'élément correspondant à l'indice i
       objective = cp.Maximize(mu @ w)
       # Définir le problème d'optimisation
       problem = cp.Problem(objective, constraints)
       # Résoudre le problème
       problem.solve()
       # L'indice de l'élément maximal
       w_MVO = w.value
       print("Le vecteur w_MVO qui maximise le gain est :", w_MVO)


def efficient_frontier(mean_returns, cov_matrix):
    num_portfolios = 2000
    results = np.zeros((3, num_portfolios))
    risk_free_rate = 0.0
    
    for i in range(num_portfolios):
        weights = np.random.random(len(mean_returns))
        weights = [random.uniform(-1, 1) for _ in range(len(mean_returns))]
        weights /= np.sum(weights)
        
        portfolio_return = np.dot(weights, mean_returns)
        portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        
        results[0,i] = portfolio_return
        results[1,i] = portfolio_std_dev
        results[2,i] = (portfolio_return - risk_free_rate) / portfolio_std_dev
    
    return results
        
        
def plot_efficient_frontier(mean_returns, cov_matrix):
    results = efficient_frontier(mean_returns, cov_matrix)
    plt.figure(figsize=(10, 6))
    plt.scatter(results[1,:], results[0,:], c=results[2,:], cmap='viridis', marker='o')
    plt.title('Efficient Frontier')
    plt.xlabel('Standard Deviation')
    plt.ylabel('Expected Return')
    plt.colorbar(label='Sharpe Ratio')
    plt.grid(True)
    plt.show()


def efficient_frontier_2(mean_returns, cov_matrix, sigma_min=0.01, sigma_max=0.15, risk_free_rate=0):
    n = int((sigma_max-sigma_min)/0.001)
    results = np.zeros((3, n+1))
    for i in range (n+1):
        vol = sigma_min + i*0.001
        w_MVO = opti_base(mean_returns, cov_matrix, risk_constraint=vol**2)
        portfolio_return = np.dot(w_MVO, mean_returns)
        results[0,i] = portfolio_return
        results[1,i] = vol
        results[2,i] = (portfolio_return - risk_free_rate) / vol
    plt.figure(figsize=(10, 6))
    plt.scatter(results[1,:], results[0,:], c=results[2,:], cmap='viridis', marker='o')
    plt.title('Efficient Frontier')
    plt.xlabel('Standard Deviation')
    plt.ylabel('Expected Return')
    plt.colorbar(label='Sharpe Ratio')
    plt.grid(True)
    plt.show()



#efficient_frontier_2(mu, Cov_matrice)


#W_MVO = opti_base()
#print(Cov_matrice @ W_MVO)

