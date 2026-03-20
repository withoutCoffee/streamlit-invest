import yfinance as yf
import streamlit as st
from utils.data import load_data, info, load_ibov_tickers, normalize_ticker, IBOV_FILE_PATH
from utils.volatility import annualized_volatility_from_prices
from utils.moving_average import bollinger
from graficos.serie import mean_avarage, plot_bollinger


def display_serie(tab):
    col1, col2 = tab.columns(2)

    period = col1.selectbox(
        "Período", options=["1y", "2y", "3y", "5y", "10y"], index=3, key="serie_period"
    )
    interval = col1.selectbox(
        "Intervalo", options=["1d", "1wk", "1mo"], index=0, key="serie_interval"
    )

    try:
        suggestions = [t.replace(".SA", "") for t in load_ibov_tickers(IBOV_FILE_PATH)]
    except Exception:
        suggestions = []

    ticker_input = col2.text_input(
        "Código da ação:",
        key="serie_ticker_input",
        placeholder="Ex: PETR4, VALE3, AAPL...",
    )
    if suggestions:
        col2.caption("Sugestões (Ibovespa): " + ", ".join(suggestions[:20]) + "...")

    confirm = tab.button("Buscar", key="serie_confirm", use_container_width=True)

    col_mm1, col_mm2, col_bb = tab.columns(3)
    mm1 = col_mm1.number_input(
        "Janela Média Móvel 1 (dias)", min_value=2, max_value=500, value=20, step=1, key="serie_mm1"
    )
    mm2 = col_mm2.number_input(
        "Janela Média Móvel 2 (dias)", min_value=2, max_value=500, value=50, step=1, key="serie_mm2"
    )
    bb_window = col_bb.number_input(
        "Janela Bollinger (dias)", min_value=2, max_value=500, value=20, step=1, key="serie_bb_window"
    )

    if not confirm:
        return

    raw = ticker_input.strip()
    if not raw:
        tab.warning("Digite o código de uma ação para pesquisar.")
        return

    ticker = normalize_ticker(raw)

    try:
        df = load_data(ticker, interval=interval, period=period)
        if df is None or df.empty:
            tab.error(
                f"Não foi possível carregar dados para **{ticker}**. "
                "Verifique o código da ação e tente novamente.",
                icon="🚨",
            )
            return

        tab.subheader("Informação da Ação e Gráfico de Preços de Fechamento Diário")
        try:
            tab.dataframe(info(ticker))
        except Exception:
            tab.info("Informações detalhadas não disponíveis para este ativo.")

        tab.line_chart(df)

        tab.subheader("Estatísticas Descritivas")
        tab.write(df.describe())

        tab.subheader("Volatilidade Anualizada")
        vol = annualized_volatility_from_prices(df["Close"])[0]
        tab.markdown(f"#### {vol}%")

        tab.subheader("Gráfico de Preço e Média Móvel")
        col_mm1 = f"MM_{mm1}"
        col_mm2 = f"MM_{mm2}"
        df[col_mm1] = df["Close"].rolling(window=mm1).mean()
        df[col_mm2] = df["Close"].rolling(window=mm2).mean()
        tab.plotly_chart(mean_avarage(df, ticker, window1=mm1, window2=mm2))

        tab.subheader("Gráfico Bandas de Bollinger")
        bodas = bollinger(df, window=bb_window)
        tab.plotly_chart(plot_bollinger(bodas, window=bb_window))

    except Exception as e:
        tab.error(f"Erro ao carregar dados da ação **{ticker}**: {e}", icon="🚨")


def display_series(tab, tickers, period, interval):
    if not tickers:
        return

    if len(tickers) == 1:
        df = load_data(ticker=tickers[0], interval=interval, period=period)
        if df is not None and not df.empty:
            tab.line_chart(df)
        return

    try:
        df = yf.download(
            tickers,
            period=period,
            interval=interval,
            progress=False,
            threads=True,
            auto_adjust=True,
        )
        tab.line_chart(df["Close"])
    except Exception as e:
        tab.write(f"Erro ao carregar dados das ações: {e}\n{tickers}")
    tab.divider()
