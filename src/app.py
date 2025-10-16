import streamlit as st
import pandas as pd
import yfinance as yf

from utils.data import load_ibov_tickers, load_data, get_close

st.title("INVESTWEB")
st.write("Aplicativo para análise de ações da bolsa Brasileira.")

#st.write(load_ibov_tickers("./data/IBOVDia_03-10-25.csv"))

# Sidebar - configurações
st.sidebar.header("Configurações")
period = st.sidebar.selectbox("Período", options=["1y", "2y", "3y", "5y", "10y"], index=3)
interval = st.sidebar.selectbox("Intervalo", options=["1d", "1wk", "1mo"], index=0)
confirm = st.sidebar.button("Confirmar")

selected_value = st.selectbox("Selecione uma ação:",load_ibov_tickers("./data/IBOVDia_03-10-25.csv"))

if confirm:
    st.sidebar.write(f"Período selecionado: {period}")
    st.sidebar.write(f"Intervalo selecionado: {interval}")

   
    df = load_data(selected_value,interval=interval, period=period)
    close_price  = pd.DataFrame(df['Close'][selected_value].values, columns=['Close'], index=df.index)

    st.line_chart(close_price)
    st.dataframe(df.tail(10))
else:

    st.sidebar.write("Aguardando confirmação...")
    st.stop()


