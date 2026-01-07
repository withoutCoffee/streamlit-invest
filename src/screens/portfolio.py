from utils.data import load_ibov_tickers, load_data
from utils.volatility import (
    annualized_volatility_from_prices,
)
import plotly.graph_objects as go
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
    multi_tickers = tab.multiselect(
        "Selecione as ações para portifólio", options=result
    )

    return multi_tickers


def display_portfolio(df):
    # 1. Tipo correto
    if not isinstance(df, pd.DataFrame):
        return False

    # 2. Não vazio
    if df.empty:
        return False

    # 3. Pelo menos uma linha e coluna
    if df.shape[0] < 1 or df.shape[1] < 1:
        return False

    # Extraindo valores da primeira (e única) linha

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df.columns,
            y=df.iloc[0] * 100,
            text=(df.iloc[0] * 100).round(2),
            textposition="outside",
        )
    )

    fig.update_layout(
        title="Lucro percentual por ativo (Buy and Hold)",
        yaxis_title="Lucro (%)",
        xaxis_title="Ticker",
    )

    return fig
