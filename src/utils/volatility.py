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

    rets = calcular_retornos(prices, returns=returns)

    vol_daily = rets.std()
    vol_annual = vol_daily * np.sqrt(252)
    vol_pct = vol_annual * 100

    return vol_pct.round(2).sort_values(ascending=False)

def calcular_retornos(prices: pd.Series, returns: str = "log") -> pd.Series:
    """
    Calcula os retornos de uma série de preços.
    - returns: "log" (retornos logarítmicos) ou "simple" (retornos percentuais)
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


def retorno_total_carteira(df, valor_inicial=1000, pesos=None):
    if df is None or df.empty:
        return None
    # Se não passar pesos, divide igualmente
    n = len(df.columns)
    if pesos is None:
        pesos = [1 / n] * n

    # Converte a linha em série se tiver apenas uma linha
    if len(df) == 1:
        df = df.iloc[0]

    # Retornos ponderados
    retorno_ponderado = sum(
        p * df[ticker]
        for p, ticker in zip(
            pesos, df.index if isinstance(df, pd.Series) else df.columns
        )
    )

    # Valor final
    valor_final = valor_inicial * (1 + retorno_ponderado)

    return valor_final, valor_final - valor_inicial


def list_stocks_by_volatility(tickers, period="1y", interval="1d"):
    volatilities = {}
    for ticker in tickers:
        df = load_data(ticker, interval=interval, period=period)
        if df is None:
            continue
        if not df.empty:
            vol = annualized_volatility_from_prices(df["Close"])
            volatilities[ticker] = vol.values[0]
    sorted_volatilities = dict(
        sorted(volatilities.items(), key=lambda item: item[1], reverse=False)
    )
    return sorted_volatilities
