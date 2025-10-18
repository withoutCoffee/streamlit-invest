from utils.data import load_ibov_tickers, load_data
from utils.volatility import annualized_volatility_from_prices

# Lista ações por volatilidade
def list_stocks_by_volatility(tickers, period="1y", interval="1d"):

    volatilities = {}
    for ticker in tickers:
        df = load_data(ticker, interval=interval, period=period)
        if not df.empty:
            vol = annualized_volatility_from_prices(df['Close'])
            volatilities[ticker] = vol.values[0]
    sorted_volatilities = dict(sorted(volatilities.items(), key=lambda item: item[1], reverse=False))
    return sorted_volatilities

def display_portfolio_volatility(period="1y", interval="1d", tab=None):

    #import streamlit as st 
    #st = tab
    tickers = load_ibov_tickers("./data/IBOVDia_03-10-25.csv")
    volatilities = list_stocks_by_volatility(tickers, period, interval)

    result = [f"{key} - {value}%" for key, value in volatilities.items()]
    
    tab.subheader("Volatilidade Anualizada das Ações da Carteira")
    multi_tickers = tab.multiselect("Selecione as ações para portifólio",result)
    return multi_tickers

