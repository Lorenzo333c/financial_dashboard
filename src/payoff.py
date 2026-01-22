import numpy as np

def call_payoff(S_T, K, premium):
    return np.maximum(S_T-K,0) - premium

#scrivo questa funzione al fine di creare un programma per computare + asset simultaneamente
#in pnls avrò come osservazioni (righe) ogni simulazione di monte carlo. mentre, come colonne
#lo strumento finanziario

def portfolio_pnl(pnls,weights):
    pnls = np.array(pnls)
    weights = np.array(weights)
    return np.dot(weights,pnls)

def put_payoff(S_T, K, premium):
    return np.maximum(K-S_T,0)-premium

def stock_payoff(S_T,S0):
    return S_T-S0

