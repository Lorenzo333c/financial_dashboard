import numpy as np

def compute_log_returns(prices):
    return np.log(prices/prices.shift(1)).dropna()

def simulate_returns(mu, sigma, T=1, n_sims=10000):
    return np.random.normal(mu * T, sigma*np.sqrt(T), n_sims)

def compute_portfolio_returns(price_data, weights):
    portfolio_returns = 0

    for symbol, w in weights.items():
        prices = price_data[symbol]["close"]
        ret = compute_log_returns(prices)
        portfolio_returns += w * ret

    return portfolio_returns
