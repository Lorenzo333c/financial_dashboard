import numpy as np

def compute_log_returns(prices):
    return np.log(prices/prices.shift(1)).dropna()

def simulate_returns(mu, sigma, T, n_sims):
    return np.random.normal(mu * T, sigma*np.sqrt(T), n_sims)