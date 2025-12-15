import plotly.graph_objects as go
import pandas as pd

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

def bollinger(data, window = 20, k=2) -> pd.DataFrame:
    df = pd.DataFrame()
    df['MM'] = data['Close'].rolling(window).mean()
    df['STD'] = data['Close'].rolling(window).std()
    df['Upper'] = df['MM'] + k * df['STD']
    df['Lower'] = df['MM'] - k * df['STD']

    df['Close'] = data['Close']
    return df

def plot_bollinger(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x = df.index,
        y = df['Close'],
        mode= 'lines',
        name='Preço Ação',
        line= dict(color='#83C9FF')
    ))
    # Média Móvel
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['MM'],
        mode='lines',
        name='MM 20',
        line=dict(color='orange', width=2)
    ))

    # Banda Superior
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Upper'],
        mode='lines',
        name='Banda Superior',
        line=dict(color='green', width=1)
    ))

    # Banda Inferior
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
        title=f'Bandas de Bollinger - Ação',
        xaxis_title='Data',
        yaxis_title='Preço',
        template='plotly_white',
        height=500
    )
    return fig