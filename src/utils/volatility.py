# utils/volatility.py
import numpy as np
import pandas as pd
from typing import Union

def annualized_volatility_from_prices(prices: Union[pd.Series, pd.DataFrame], returns: str = "log") -> pd.Series:
    """
    Recebe preços (Series ou DataFrame) e retorna volatilidade anualizada em % (com 2 casas).
    - returns: "log" (retornos log) ou "simple" (retornos percentuais)
    """
    if isinstance(prices, pd.Series):
        prices = prices.to_frame()

    if prices.empty:
        return pd.Series(dtype=float)

    if returns == "log":
        rets = np.log(prices / prices.shift(1)).dropna()
    else:
        rets = prices.pct_change().dropna()

    vol_daily = rets.std()
    vol_annual = vol_daily * np.sqrt(252)
    vol_pct = vol_annual * 100
    return vol_pct.round(2).sort_values(ascending=False)
