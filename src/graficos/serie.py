import plotly.graph_objects as go


def mean_avarage(dados, ticker, window1=20, window2=50):
    col1 = f"MM_{window1}"
    col2 = f"MM_{window2}"

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dados.index,
        y=dados['Close'],
        mode='lines',
        name=f'Preço {ticker}'
    ))
    fig.add_trace(go.Scatter(
        x=dados.index,
        y=dados[col1],
        mode='lines',
        name=f'Média Móvel {window1}D',
        line=dict(color='orange')
    ))
    fig.add_trace(go.Scatter(
        x=dados.index,
        y=dados[col2],
        mode='lines',
        name=f'Média Móvel {window2}D',
        line=dict(color='#FF6692')
    ))

    fig.update_layout(
        title=f'Série Temporal - {ticker} com Médias Móveis {window1}D e {window2}D',
        xaxis_title='Data',
        yaxis_title='Preço',
        hovermode='x unified'
    )
    return fig


def plot_bollinger(df, window=20):
    mm_col = f'MM_{window}'
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
        y=df[mm_col],
        mode='lines',
        name=f'MM {window}',
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
