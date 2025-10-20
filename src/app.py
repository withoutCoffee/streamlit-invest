
import streamlit as st
from screens.serie import display_series
from utils.data import load_ibov_tickers

from screens.portfolio import display_portfolio_volatility, retorno_total_carteira
from utils.volatility import calcular_retorno_carteira


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
    multi_tickers = display_portfolio_volatility(period=period, interval=interval, tab=tab2)
    selected_tickers = list(map(lambda x: x.split(" - ")[0], multi_tickers))
    # Graficos 
    display_series(tab2,selected_tickers, period, interval)

    # retorno da carteira
    st.subheader("Retorno das ações da carteira")
    ret_total = calcular_retorno_carteira(selected_tickers, period=period, interval=interval)
    st.dataframe(ret_total)

    st.write("Retorno de investimento da carteira: de R$1000 e divisão igualitária entre os ativos.")
    valor_final, lucro = retorno_total_carteira(ret_total, valor_inicial=1000)
    st.markdown(f"Valor final: **RS {valor_final:.2f}**, Lucro: **RS {lucro:.2f}**")
    


    
 



