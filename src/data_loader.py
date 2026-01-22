import pandas as pd

def load_market_data(path):
    df = pd.read_csv(path, parse_dates=['date'])
    df = df.sort_values('date')
    return df