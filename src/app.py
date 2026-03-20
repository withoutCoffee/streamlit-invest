from datetime import datetime, timedelta
import os

import streamlit as st

from utils.data import IBOV_FILE_PATH
from utils.volatility import calcular_retorno_carteira, retorno_total_carteira

from screens.serie import display_serie, display_series
from screens.portfolio import display_portfolio_volatility
from graficos.portfolio import display_portfolio

# sempre que o app for iniciado verificar se tem o arquivo atualizado, se tiver mais de 5 dias do último download, baixar o arquivo atualizado
from database.collect import download_ibov_tickers

# Verificar se o arquivo de tickers do IBOV está atualizado
if not os.path.exists(IBOV_FILE_PATH) or (datetime.now() - datetime.fromtimestamp(os.path.getmtime(IBOV_FILE_PATH))) > timedelta(days=5):
    download_ibov_tickers("https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br", IBOV_FILE_PATH)


def get_markdown(path):
    with open(path, "r", encoding="UTF-8") as f:
        return f.read()


st.title("INVESTWEB")
st.write("Aplicativo para análise de ações da bolsa Brasileira.")
st.markdown('_As ações listadas aqui são ações da Ibovespa, por serem ações com mais liquidez._')

tab1, tab2, tab3 = st.tabs(["Análise de Ação", "Simulação de Carteira", "Guia Rapido"])

tab3.markdown(get_markdown("./data/info.md"))

with tab1:
    display_serie(tab1)

with tab2:
    col1, col2 = st.columns(2)

    p = col1.selectbox(
        "Período", options=["1y", "2y", "3y", "5y", "10y"], index=0, key="selectbox_4"
    )
    i = col2.selectbox(
        "Intervalo", options=["1d", "1wk", "1mo"], index=0, key="selectbox_5"
    )

    selected_tickers = display_portfolio_volatility(period=p, interval=i, tab=tab2)

    # Gráficos de série temporais de preços das ações selecionadas
    display_series(tab2, selected_tickers, p, i)

    # Retorno da carteira
    st.subheader("Retorno das ações da carteira")
    ret_total = calcular_retorno_carteira(
        selected_tickers, period=p, interval=i
    )
    #st.dataframe(ret_total)

    fig = display_portfolio(ret_total)
    if fig :
        st.plotly_chart(fig)

    number = st.number_input("Valor inicial de investimento inicial:", value=1000)
    st.write(
        f"Retorno de investimento da carteira: de R${number} e divisão igualitária entre os ativos."
    )
    try:
        valor_final, lucro = retorno_total_carteira(ret_total, valor_inicial=number)
        st.markdown(f"Valor final: **RS {valor_final:.2f}**\n Lucro: **RS {lucro:.2f}**")
    except Exception as e:
        st.write(f"Erro ao calcular retorno da carteira: {e}")
