import yfinance as yf
from utils.data import load_data, info
from utils.volatility import annualized_volatility_from_prices
from utils.moving_average import bollinger
from graficos.serie import mean_avarage, plot_bollinger


# Display de tab1 confirmada
def display_serie(tab, selected_value, period, interval):
    st = tab

    # informações da ação
    try:
        df = load_data(selected_value, interval=interval, period=period)
        # Gráfico de preços
        st.subheader("Informação da Ação e Gráfico de Preços de Fechamento Diário")

        st.dataframe(info(selected_value))
        st.line_chart(df)

        #
        st.subheader("Estatísticas Descritivas")
        st.write(df.describe())
        st.subheader("Volatilidade Anualizada")
        vol = annualized_volatility_from_prices(df["Close"])[0]
        st.markdown(f"#### {vol}%")
        #
        st.subheader("Gráfico de Preço e Média Móvel")
        df["MM_20"] = df["Close"].rolling(window=20).mean()
        df["MM_50"] = df["Close"].rolling(window=50).mean()
        st.plotly_chart(mean_avarage(df, selected_value))
        # Bodas de bolinger
        st.subheader("Gráfico Bodas de Bollinger")
        bodas = bollinger(df)
        st.plotly_chart(plot_bollinger(bodas))

    except Exception as e:
        st.error(f"Erro ao carregar dados da ação:{e}", icon="🚨")


# Display de tab1 confirmada
def display_series(tab, tickers, period, interval):
    st = tab
    if len(tickers) == 1:
        df = load_data(ticker=tickers[0], interval=interval, period=period)
        st.line_chart(df)
        return

    # informações da ação
    try:
        df = yf.download(
            tickers,
            period=period,
            interval=interval,
            progress=False,
            threads=True,
            auto_adjust=True,
        )
        # Gráfico de preços
        st.line_chart(df["Close"])
    except Exception as e:
        st.write(f"Erro ao carregar dados das ações:{e}\n{tickers}")
    st.divider()
