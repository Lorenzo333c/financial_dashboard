import pandas as pd
import yfinance as yf

def load_yahoo_data(symbol, start_date, end_date):   
    df = yf.download(
        symbol,
        start=start_date,
        end=end_date,
        progress=False,
        auto_adjust=True
    )
    if df.empty:
        return None
#normalizzare nomi delle colonne
    df = df.reset_index()
    df.columns = [c.lower() for c in df.columns]
    return df

#scaricare dati da YF, più ticker alla volta
def load_multiple_yahoo_data(symbols, start_date, end_date):
    
    data = {}

    for symbol in symbols:
        df = load_yahoo_data(symbol, start_date, end_date)
        if df is not None and "close" in df.columns:
            data[symbol] = df

    return data
