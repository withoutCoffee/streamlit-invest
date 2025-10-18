import plotly.graph_objects as go

def mean_avarage(dados,ticker):
    # 3. Criar figura no Plotly
    fig = go.Figure()
    # Série de Preço
    fig.add_trace(go.Scatter(
        x=dados.index, 
        y=dados['Close'], 
        mode='lines', 
        name=f'Preço {ticker}'
    ))

    # Média Móvel
    fig.add_trace(go.Scatter(
        x=dados.index, 
        y=dados['MM'], 
        mode='lines', 
        name='Média Móvel',
        line=dict(color='orange')
    ))

    # Layout
    fig.update_layout(
        title=f'Série Temporal - {ticker} com Média Móvel 20D',
        xaxis_title='Data',
        yaxis_title='Preço',
        hovermode='x unified'  # tooltip inteligente
    )
    return fig