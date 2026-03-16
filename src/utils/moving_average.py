import pandas as pd


def bollinger(data, window=20, k=2) -> pd.DataFrame:
    df = pd.DataFrame()
    df[f'MM_{window}'] = data['Close'].rolling(window).mean()
    df['STD'] = data['Close'].rolling(window).std()
    df['Upper'] = df[f'MM_{window}'] + k * df['STD']
    df['Lower'] = df[f'MM_{window}'] - k * df['STD']

    df['Close'] = data['Close']
    return df