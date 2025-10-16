import streamlit as st
from utils.data import load_ibov_tickers, load_data, info
from utils.volatility import annualized_volatility_from_prices
from screens.serie import mean_avarage


st.title("INVESTWEB")
st.write("Aplicativo para análise de ações da bolsa Brasileira.")

tab1, tab2 = st.tabs(["Análise de Ação", "Simulação de Carteira"])

# Sidebar - configurações
st.sidebar.header("Configurações")
period = st.sidebar.selectbox("Período", options=["1y", "2y", "3y", "5y", "10y"], index=3)
interval = st.sidebar.selectbox("Intervalo", options=["1d", "1wk", "1mo"], index=0)
confirm = st.sidebar.button("Confirmar")


selected_value = tab1.selectbox("Selecione uma ação:",load_ibov_tickers("./data/IBOVDia_03-10-25.csv"))

if confirm:
    st.sidebar.write(f"Período selecionado: {period}")
    st.sidebar.write(f"Intervalo selecionado: {interval}")

    tab1.dataframe(info(selected_value))
   
    df = load_data(selected_value,interval=interval, period=period)

    tab1.line_chart(df)
    
    

    tab1.subheader("Gráfico de Preço e Média Móvel")
    df['MM'] = df['Close'].rolling(window=20).mean()
    tab1.plotly_chart(mean_avarage(df,selected_value))
    

    tab1.subheader("Estatísticas Descritivas")
    tab1.write(df.describe())
    tab1.subheader("Volatilidade Anualizada")
    
    vol = annualized_volatility_from_prices(df['Close'])
    tab1.write(vol)
else:

    st.sidebar.write("Aguardando confirmação...")
    st.stop()


