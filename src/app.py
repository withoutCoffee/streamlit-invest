import streamlit as st
from utils.data import load_ibov_tickers, load_data, info
from utils.volatility import annualized_volatility_from_prices
from utils.moving_average import mean_avarage

from screens.portfolio import display_portfolio_volatility


def get_markdown(path):

    with open(path, "r", encoding="UTF-8") as f:
        return  f.read()


st.title("INVESTWEB")
st.write("Aplicativo para análise de ações da bolsa Brasileira.")

tab1, tab2, tab3= st.tabs(["Análise de Ação", "Simulação de Carteira","Guia Rapido"])

# Sidebar - configurações
st.sidebar.header("Configurações")

period = st.sidebar.selectbox("Período", options=["1y", "2y", "3y", "5y", "10y"], index=3)
interval = st.sidebar.selectbox("Intervalo", options=["1d", "1wk", "1mo"], index=0)

tab3.markdown(get_markdown("./data/info.md"))


with tab1:
    selected_value = st.selectbox("Selecione uma ação:", load_ibov_tickers("./data/IBOVDia_03-10-25.csv"))
    confirm = st.button("Confirmar")
    if confirm:
        st.sidebar.write(f"Período selecionado: {period}")
        st.sidebar.write(f"Intervalo selecionado: {interval}")
        
        from screens.serie import display_serie
        display_serie(tab1, selected_value, period, interval)
    else:
        st.sidebar.write("Aguardando confirmação...") 

with tab2:
    tickers = display_portfolio_volatility(period=period, interval=interval, tab=tab2)
    st.write(tickers)


    
 



