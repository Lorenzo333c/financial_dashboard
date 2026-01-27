import pandas as pd
import yfinance as yf

import yfinance as yf
import pandas as pd

def load_yahoo_data(symbol, start_date, end_date):
        
    df = yf.download(
        symbol,
        start=start_date,
        end=end_date,
        progress=False
    )

    df = df.reset_index()
    df.columns = [c.lower() for c in df.columns]

    return df

def load_multiple_yahoo_data(symbols, start_date, end_date):
    
    data = {}

    for symbol in symbols:
        df = load_yahoo_data(symbol, start_date, end_date)
        if not df.empty:
            data[symbol] = df

    return data
