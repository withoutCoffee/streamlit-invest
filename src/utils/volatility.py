# utils/volatility.py
import numpy as np
import pandas as pd
from typing import Union
import yfinance as yf

from utils.data import load_data

def annualized_volatility_from_prices(prices: Union[pd.Series, pd.DataFrame], returns: str = "log") -> pd.Series:
    """
    Recebe preços (Series ou DataFrame) e retorna volatilidade anualizada em % (com 2 casas).
    - returns: "log" (retornos log) ou "simple" (retornos percentuais)
    """
    if isinstance(prices, pd.Series):
        prices = prices.to_frame()

    if prices.empty:
        return pd.Series(dtype=float)

    rets = profit(prices, returns = returns)

    vol_daily = rets.std()
    vol_annual = vol_daily * np.sqrt(252)
    vol_pct = vol_annual * 100

    return vol_pct.round(2).sort_values(ascending=False)

def profit(prices: pd.Series, returns: str = "log") -> float:
    """
    Calcula o lucro percentual de uma série de preços.
    """
    if prices.empty:
        return pd.Series(dtype=float)

    if returns == "log":
        return np.log(prices / prices.shift(1)).dropna()
    else:
        return prices.pct_change().dropna()
    
def calcular_retorno_carteira(tickers, period="1y", interval="1d"):
  
    retornos_individuais = {}
    for ticker in tickers:
        df = load_data(ticker, interval=interval, period=period)
        if df is None:
            continue
        if not df.empty:
            retorno = (df.iloc[-1] / df.iloc[0]) - 1
            retornos_individuais[ticker] = retorno

    return pd.DataFrame(retornos_individuais)