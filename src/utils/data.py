import streamlit as st 
import pandas as pd 
import yfinance as yf 
from typing import List


def normalize_ticker(t: str) -> str:
    """Normaliza ticker para o padrão Yahoo (adiciona .SA quando apropriado)."""
    s = t.strip().upper()
    if not s:
        return s
    # se já tem ponto (ex: BVMF:PETR4 ou AAPL) não alteramos; para B3 usamos .SA
    if '.' not in s:
        s = s + '.SA'
    return s

def normalize_tickers(tickers: List[str]) -> List[str]:
    return [normalize_ticker(t) for t in tickers if isinstance(t, str) and t.strip()]

@st.cache_data
def load_ibov_tickers(path:str) -> list:
    ibov_tickers = pd.read_csv(path, encoding= 'latin1', sep=';', skiprows=1)
    ibov_tickers = ibov_tickers.index
    ibov_tickers = normalize_tickers(ibov_tickers)

    return ibov_tickers[:-2] # Duas últimas linhas não são tickers válidos

@st.cache_data
def load_data(ticker:str, period: str = "5y", interval: str = "1d", chunk_size: int = 50) -> pd.DataFrame:
    try:
        df = yf.download(ticker, period=period, interval=interval, progress=False, threads=True)
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
