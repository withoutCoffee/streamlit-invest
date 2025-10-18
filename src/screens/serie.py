
# Display de tab1 confirmada
def display_serie(tab, selected_value, period, interval):
    import streamlit as st
    from utils.data import load_data, info
    from utils.volatility import annualized_volatility_from_prices
    from utils.moving_average import mean_avarage

    st = tab

    # informações da ação
    st.dataframe(info(selected_value))
    df = load_data(selected_value, interval=interval, period=period)
    
    # Gráfico de preços
    st.line_chart(df)
    
    st.subheader("Gráfico de Preço e Média Móvel")
    df['MM'] = df['Close'].rolling(window=20).mean()
    st.plotly_chart(mean_avarage(df, selected_value))
    
    st.subheader("Estatísticas Descritivas")
    st.write(df.describe())

    st.subheader("Volatilidade Anualizada")
    vol = annualized_volatility_from_prices(df['Close'])[0]
    st.write(f"{vol}")