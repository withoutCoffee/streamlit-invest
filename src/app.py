import streamlit as st
import pandas as pd
import yfinance as yf


@st.cache_data
def carregar_dados(ticker):
    ticker = ticker.upper() + '.SA'
    dados = yf.download(ticker, start='2010-01-01', end='2025-10-07')
    dados.reset_index(inplace=True)
    return dados

print(carregar_dados('ITUB4'))

st.write("""# App de ações 
         Mostra série temporal do preço de fechamento, 
         além de estatísticas importantes para previsão da série.
         """) # markdown

# Gráficos 
#st.table(carregar_dados('ITUB4'))

st.write("""# Fim do App
         """) # markdown



