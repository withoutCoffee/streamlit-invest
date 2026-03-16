import plotly.graph_objects as go


def mean_avarage(dados, ticker):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dados.index,
        y=dados['Close'],
        mode='lines',
        name=f'Preço {ticker}'
    ))
    fig.add_trace(go.Scatter(
        x=dados.index,
        y=dados['MM_20'],
        mode='lines',
        name='Média Móvel 20D',
        line=dict(color='orange')
    ))
    fig.add_trace(go.Scatter(
        x=dados.index,
        y=dados['MM_50'],
        mode='lines',
        name='Média Móvel 50D',
        line=dict(color='#FF6692')
    ))

    fig.update_layout(
        title=f'Série Temporal - {ticker} com Média Móvel 20D',
        xaxis_title='Data',
        yaxis_title='Preço',
        hovermode='x unified'
    )
    return fig


def plot_bollinger(df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Close'],
        mode='lines',
        name='Preço Ação',
        line=dict(color='#83C9FF')
    ))
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['MM_20'],
        mode='lines',
        name='MM 20',
        line=dict(color='orange', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Upper'],
        mode='lines',
        name='Banda Superior',
        line=dict(color='green', width=1)
    ))
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Lower'],
        mode='lines',
        name='Banda Inferior',
        line=dict(color='red', width=1),
        fill='tonexty',
        fillcolor='rgba(150,150,150,0.3)'
    ))

    fig.update_layout(
        title='Bandas de Bollinger - Ação',
        xaxis_title='Data',
        yaxis_title='Preço',
        template='plotly_white',
        height=500
    )
    return fig
