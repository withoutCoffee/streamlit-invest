import plotly.graph_objects as go
import pandas as pd


def display_portfolio(df):
    if not isinstance(df, pd.DataFrame):
        return False

    if df.empty:
        return False

    if df.shape[0] < 1 or df.shape[1] < 1:
        return False

    labels = df.columns
    values = df.iloc[0].values
    cores = ["green" if v >= 0 else "red" for v in values]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=labels,
            y=values * 100,
            marker=dict(color=cores),
            text=[f"{v:.2%}" for v in values],
            textposition="auto",
        )
    )

    fig.update_layout(
        title="Lucro percentual por ativo (Buy and Hold)",
        yaxis_title="Lucro (%)",
        xaxis_title="Ticker",
    )

    return fig
