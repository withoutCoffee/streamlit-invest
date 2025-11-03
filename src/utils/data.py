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
def load_data(ticker:str, period: str = "1y", interval: str = "1d", chunk_size: int = 50) -> pd.DataFrame:
    try:
        df = yf.download(ticker, period=period, interval=interval, progress=False, threads=True, auto_adjust=True)
        return pd.DataFrame(df['Close'][ticker].values, columns=['Close'], index=df.index)
    except Exception as e:
        print(f"Erro ao baixar dados para {ticker}: {e}")
    return 


@st.cache_data
def info(ticker:str)-> pd.DataFrame:
    """
    Busca informações principais de uma ação usando yfinance.
    
    Parâmetros:
        ticker (str): Exemplo "PETR4.SA"
    
    Retorna:
        DataFrame com detalhes da empresa
    """
    acao = yf.Ticker(ticker)
    info = acao.info  # Pega dicionário com as informações

    # Monta um dicionário com os campos mais relevantes
    dados = {
        "Ticker": info.get("symbol", ticker),
        "Nome": info.get("longName", "N/A"),
        "Setor": info.get("sector", "N/A"),
        "Subsetor": info.get("industry", "N/A"),
        "Preço Atual": acao.history(period="1d")["Close"].iloc[-1] if not acao.history(period="1d").empty else None,
        "Valor de Mercado": info.get("marketCap", "N/A"),
        "P/L (Trailing PE)": info.get("trailingPE", "N/A"),
        "Dividend Yield": info.get("dividendYield", 0) if info.get("dividendYield") else 0,
        "Beta": info.get("beta", "N/A")
    }
    # Converte para DataFrame vertical
    df_vertical = pd.DataFrame.from_dict(dados, orient='index', columns=['Valor'])
    return df_vertical
