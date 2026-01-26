import numpy as np

def compute_log_returns(prices):
    return np.log(prices/prices.shift(1)).dropna()

def simulate_returns(mu, sigma, T, n_sims):
    return np.random.normal(mu * T, sigma*np.sqrt(T), n_sims)

def compute_portfolio_returns(price_data, weights):
    import pandas as pd

    returns = []

    for symbol, w in weights.items():
        log_ret = compute_log_returns(price_data[symbol]["close"])
        returns.append(w * log_ret)

    portfolio_returns = sum(returns)
    return portfolio_returns
