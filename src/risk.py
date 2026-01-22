import numpy as np

def expected_shortfall(pnl, alpha = 5):
    threshold = var(pnl,alpha)
    return pnl[pnl <= threshold].mean()

def var (pnl, alpha = 5):
    return np.percentile(pnl,alpha)