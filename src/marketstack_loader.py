import pandas as pd
import requests

def load_marketstack_data(
        api_key,
        symbol,
        start_date,
        end_date
):
    url = "http://api.marketstack.com/v1/eod"
    params = {
        'access_key': api_key,
        'symbols': symbol,
        'date_from': start_date,
        'date_to': end_date,
        'limit': 2000
    }

    response = requests.get(url, params = params)
    data = response.json()

    df = pd.DataFrame(data['data'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    return df

def load_multiple_marketstack_data(api_key,symbols,start_date, end_date):
    import pandas as pd

    dfs = {}

    for symbol in symbols:
        df = load_marketstack_data(
            api_key,
            symbol,
            start_date,
            end_date
        )
        dfs[symbol] = df
    return dfs
    