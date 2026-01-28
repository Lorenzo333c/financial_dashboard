import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from src.analytics import compute_log_returns, simulate_returns,compute_portfolio_returns 
from src.payoff import call_payoff, portfolio_pnl, stock_payoff, put_payoff
from src.risk import var, expected_shortfall
from src.data_loader import load_yahoo_data, load_multiple_yahoo_data

# TITOLO
st.title("Dashboard finanziaria – Monte Carlo")
st.write("Simulazione semplice di un payoff tramite Monte Carlo")

# INPUT UTENTE
st.header("Parametri di input")

S0 = st.number_input("Prezzo iniziale dell'asset", value=100.0)
n_sims = st.number_input("Numero simulazioni", value=10000, step=1000)

#Date
import datetime as dt
st.sidebar.header("Dati di mercato")
start_date = st.sidebar.date_input("Data inizio")
end_date = st.sidebar.date_input("Data fine")

#Portafoglio
st.header("Posizioni di portafoglio")

positions_df = st.data_editor(
    pd.DataFrame({
        "Ticker": ["META", "NVDA"],
        "Quantità": [150, 200]
    }),
    num_rows="dynamic"
)

#filtraggio dati-input estratti 
positions_df = positions_df.dropna()
positions_df["Ticker"] = positions_df["Ticker"].str.strip().str.upper()
positions_df["Quantità"] = positions_df["Quantità"].astype(float)

#nuova
symbols = positions_df["Ticker"].tolist()
price_data = load_multiple_yahoo_data(symbols, start_date, end_date)
if not price_data:
    st.error("Nessun dato disponibile per i ticker selezionati.")
    st.stop()

valid_symbols = list(price_data.keys())
positions_df = positions_df[positions_df['Ticker'].isin(valid_symbols)]

symbols = positions_df['Ticker'].tolist()
quantities = positions_df['Quantità'].values

latest_prices = {s: price_data[s]['close'].iloc[-1] for s in symbols}

#valore portafoglio
portfolio_value = sum(
    latest_prices[s] * q
    for s, q in zip(symbols, quantities)
)

st.metric("Valore attuale del portafoglio", f"{portfolio_value:,.2f} €")

#Pesi portafoglio
weights = {
    s: (latest_prices[s] * q) / portfolio_value
    for s, q in zip(symbols, quantities)}

#ritorni ponderati
portfolio_returns = compute_portfolio_returns(price_data, weights)

mu = portfolio_returns.mean()
sigma = portfolio_returns.std()

#Monte Carlo
simulated_returns = np.random.normal(mu, sigma, int(n_sims))
portfolio_values_T = portfolio_value * np.exp(simulated_returns)
pnl_portfolio = portfolio_values_T - portfolio_value

fig, ax = plt.subplots()
ax.hist(pnl_portfolio, bins=50)
ax.set_title("Distribuzione P&L Portafoglio")
ax.set_xlabel("P&L")
ax.set_ylabel("Frequenza")
st.pyplot(fig)

#Opzioni
st.header("Opzioni")

K = st.number_input('Strike della CALL', value = 100.0)
premium = st.number_input('Premio pagato', value = 5.0)

sim_ret = simulate_returns(mu, sigma, T = 1, n_sims=n_sims)
S_T =S0 *np.exp(sim_ret)

pnl_stock = stock_payoff(S_T, S0)
pnl_call = call_payoff(S_T, K, premium)
pnl_put = put_payoff(S_T, K, premium)

#placeholder
payoff_call = np.maximum(S_T - K, 0) - premium

st.header('Distribuzione del payoff (P&L)')

fig2, ax2 = plt.subplots()
ax2.hist(payoff_call, bins = 50)
ax2.set_xlabel('Profit & Loss')
ax2.set_ylabel('Frequenza')
st.pyplot(fig2)
#

#placeholder
fig, ax = plt.subplots()
ax.hist(S_T, bins=50)
ax.set_xlabel("Prezzo finale")
ax.set_ylabel("Frequenza")
st.pyplot(fig)
#

#pesi degli strumenti (short se negativo)
w_stock = st.slider('Peso Azione', -2.0, 2.0,1.0)
w_call = st.slider('Peso Call',-2.0, 2.0,1.0)
w_put = st.slider('Peso Put', -2.0, 2.0,1.0)
portfolio_pnls_mc = portfolio_pnl(
    [pnl_stock,pnl_call, pnl_put],
    [w_stock, w_call, w_put]
)

# GRAFICO
st.header("Distribuzione dei prezzi simulati")

figt, ax = plt.subplots()
ax.hist(portfolio_pnls_mc, bins =50)
ax.set_title('Distribuzione P&L Strumenti')
ax.set_xlabel('P&L')
ax.set_ylabel('Frequenza')
st.pyplot(figt)

#grafico distribuzione di ritorni portafoglio x strumento
fig, ax = plt.subplots()
ax.hist(pnl_stock, bins=50, alpha=0.5, label="Stock")
ax.hist(pnl_call, bins=50, alpha=0.5, label="Call")
ax.hist(portfolio_pnls_mc, bins=50, alpha=0.7, label="Portfolio")
ax.legend()
st.pyplot(fig)

VaR_5 = var(portfolio_pnls_mc)
ES_5 = expected_shortfall(portfolio_pnls_mc)

st.metric("VaR Portafoglio (5%)", f"{VaR_5:.2f} €")
st.metric("ES Portafoglio (5%)", f"{ES_5:.2f} €")




