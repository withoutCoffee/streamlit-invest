import streamlit as st 
import pandas as pd 
import yfinance as yf 

@st.cache_data
def load_ibov_tickers(path:str) -> list:
    ibov_tickers = pd.read_csv(path, encoding= 'latin1', sep=';', skiprows=1)
    ibov_tickers = ibov_tickers.index
    ibov_tickers = list(map(lambda x: x+'.SA', ibov_tickers))

    return ibov_tickers[:-2] # Duas últimas linhas não são tickers válidos

@st.cache_data
def load_data(ticker:str, i:str = '2019-01-01', f:str = '2024-12-31') -> pd.DataFrame:
    try:
        df = yf.download(ticker, start= i, end= f)
        #df.reset_index(inplace=True)
        #df.set_index('Date', inplace=True)
        
        return df
    except Exception as e:
        print(f"Erro ao baixar dados para {ticker}: {e}")
    return 

@st.cache_data
def get_close(data):
    df = data['Close']
    df.index = data['Date']
    return df
