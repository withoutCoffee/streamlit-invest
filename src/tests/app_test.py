import streamlit as st
import pandas as pd
import yfinance as yf
from utils_test.data import load_ibov_tickers, load_data, get_close


#print(load_ibov_tickers("./data/IBOVDia_03-10-25.csv"))

st.title("Testando App de Ações")
st.write("Aplicativo para análise e verificação de rentabilidade de ações da bolsa Brasileira.")

#st.write(load_ibov_tickers("./data/IBOVDia_03-10-25.csv"))

selected_value = st.selectbox("Selecione uma ação:",load_ibov_tickers("./data/IBOVDia_03-10-25.csv"))

#tab1, tab2 = st.tabs(['Tabela', 'Gráfico'])

serie = load_data(selected_value)
close_price  = pd.DataFrame(serie['Close'][selected_value].values, columns=['Close'], index=serie.index)

st.line_chart(close_price)
st.dataframe(serie)



