import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from src.data_loader import load_market_data
from src.analytics import compute_log_returns, simulate_returns
from src.payoff import call_payoff, portfolio_pnl, stock_payoff, put_payoff
from src.risk import var, expected_shortfall


# TITOLO
st.title("Dashboard finanziaria – Monte Carlo")

st.write("Simulazione semplice di un payoff tramite Monte Carlo")

# INPUT UTENTE
st.header("Parametri di input")

S0 = st.number_input("Prezzo iniziale dell'asset", value=100.0)
mu = st.number_input("Rendimento medio annuo", value=0.05)
sigma = st.number_input("Volatilità annua", value=0.2)
n_sims = st.number_input("Numero simulazioni", value=10000, step=1000)

# SIMULAZIONE MONTE CARLO
st.header("Simulazione")

simulated_returns = np.random.normal(mu, sigma, int(n_sims))
S_T = S0 * np.exp(simulated_returns)

# GRAFICO
st.header("Distribuzione dei prezzi simulati")

fig, ax = plt.subplots()
ax.hist(S_T, bins=50)
ax.set_xlabel("Prezzo finale")
ax.set_ylabel("Frequenza")

st.pyplot(fig)

#opzione

st.header("Parametri dell'opzione")

K = st.number_input('Strike della CALL', value = 100.0)
premium = st.number_input('Premio pagato', value = 5.0)

S_T = S0 * np.exp(simulated_returns)

payoff_call = np.maximum(S_T - K, 0) - premium

st.header('Distribuzione del payoff (P&L)')

fig2, ax2 = plt.subplots()
ax2.hist(payoff_call, bins = 50)
ax2.set_xlabel('Profit & Loss')
ax2.set_ylabel('Frequenza')

st.pyplot(fig2)

sim_ret = simulate_returns(mu, sigma, T = 1, n_sims=n_sims)
S_T =S0 *np.exp(sim_ret)

pnl_stock = stock_payoff(S_T, S0)
pnl_call = call_payoff(S_T, K, premium)
pnl_put = put_payoff(S_T, K, premium)

#pesi degli strumenti (short se negativo)
w_stock = st.slider('Peso AZione', -2.0, 2.0,1.0)
w_call = st.slider('Peso Call',-2.0, 2.0,1.0)
w_put = st.slider('Peso Put', -2.0, 2.0,1.0)

portfolio_pnls_mc = portfolio_pnl(
    [pnl_stock,pnl_call, pnl_put],
    [w_stock, w_call, w_put]
)

fig, ax = plt.subplots()
ax.hist(portfolio_pnls_mc, bins =50)
ax.set_title('Distribuzione P&L Portfolio')
ax.set_xlabel('P&L')
ax.set_ylabel('Frequenza')
st.pyplot(fig)

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




