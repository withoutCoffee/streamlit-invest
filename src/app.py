import streamlit as st

from utils.data import load_ibov_tickers, get_selic
from utils.volatility import calcular_retorno_carteira, retorno_total_carteira

from screens.serie import display_serie
from screens.portfolio import display_portfolio_volatility
from screens.serie import display_series


def get_markdown(path):
    with open(path, "r", encoding="UTF-8") as f:
        return f.read()


st.title("INVESTWEB")
st.write("Aplicativo para análise de ações da bolsa Brasileira.")
st.markdown('_As ações listadas aqui são ações da Ibovespa, por serem ações com mais liquidez._')

tab1, tab2, tab3 = st.tabs(["Análise de Ação", "Simulação de Carteira", "Guia Rapido"])

tab3.markdown(get_markdown("./data/info.md"))

with tab1:
    col1, col2 = st.columns(2)

    period = col1.selectbox(
        "Período", options=["1y", "2y", "3y", "5y", "10y"], index=3, key="selectbox_1"
    )
    interval = col1.selectbox(
        "Intervalo", options=["1d", "1wk", "1mo"], index=0, key="selectbox_2"
    )

    selected_value = col2.selectbox(
        "Selecione uma ação:",
        load_ibov_tickers("./data/IBOVDia_03-10-25.csv"),
        key="selectbox_3",
    )
    confirm = st.button("Confirmar", width="stretch", key="button_1")

    if confirm:
        col2.write(f"Período selecionado: {period}")
        col2.write(f"Intervalo selecionado: {interval}")
        display_serie(tab1, selected_value, period, interval)
    else:
        col2.write("Aguardando confirmação...")

with tab2:
    col1, col2 = st.columns(2)

    p = col1.selectbox(
        "Período", options=["1y", "2y", "3y", "5y", "10y"], index=0, key="selectbox_4"
    )
    i = col2.selectbox(
        "Intervalo", options=["1d", "1wk", "1mo"], index=0, key="selectbox_5"
    )

    # Seleção de ações por volatilidade
    multi_tickers = display_portfolio_volatility(period=p, interval=i, tab=tab2)

    selected_tickers = list(
        map(lambda x: x.split(" - ")[0], multi_tickers)
    )  # retira o valor da volatilidade

    # Graficos se série temporais de preços das ações selecionadas
    display_series(tab2, selected_tickers, period, interval)

    # Retorno da carteira
    st.subheader("Retorno das ações da carteira")
    ret_total = calcular_retorno_carteira(
        selected_tickers, period=period, interval=interval
    )
    st.dataframe(ret_total)

    number = st.number_input("Valor inicial de investimento inicial:", value=1000)
    st.write(
        "Retorno de investimento da carteira: de R$1000 e divisão igualitária entre os ativos."
    )
    try:
        valor_final, lucro = retorno_total_carteira(ret_total, valor_inicial=number)
        st.markdown(f"Valor final: **RS {valor_final:.2f}**, Lucro: **RS {lucro:.2f}**")

        # retorno_selic = calcular_retorno_carteira(
        #     get_selic(period=int(period.split('y')[0])), period=period, interval=interval
        # )
        # st.markdown(f"Valor selic: **RS {retorno_selic:.2f}")
    except Exception as e:
        st.write(f"Erro ao calcular retorno da carteira: {e}")
