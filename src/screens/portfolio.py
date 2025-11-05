from utils.data import load_ibov_tickers, load_data
from utils.volatility import (
    annualized_volatility_from_prices,
)
import pandas as pd


# Lista ações por volatilidade
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


def display_portfolio_volatility(tab=None, period="1y", interval="1d"):

    tickers = load_ibov_tickers("./data/IBOVDia_03-10-25.csv")
    volatilities = list_stocks_by_volatility(tickers, period, interval)

    result = [f"{key} - {value}%" for key, value in volatilities.items()]

    tab.subheader("Volatilidade Anualizada das Ações da Carteira - Ibov")
    multi_tickers = tab.multiselect("Selecione as ações para portifólio", options = result)

    return multi_tickers


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
