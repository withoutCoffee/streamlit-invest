from utils.data import load_ibov_tickers
from utils.volatility import list_stocks_by_volatility


def display_portfolio_volatility(tab=None, period="1y", interval="1d"):
    tickers = load_ibov_tickers("./data/IBOVDia_03-10-25.csv")
    volatilities = list_stocks_by_volatility(tickers, period, interval)

    result = [f"{key} - {value}%" for key, value in volatilities.items()]

    tab.subheader("Volatilidade Anualizada das Ações da Carteira - Ibov")
    multi_tickers = tab.multiselect(
        "Selecione as ações para portifólio", options=result
    )

    return multi_tickers
