# Metrics, returns, volatility

import pandas as pd
import numpy as np

def calculate_daily_returns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Return"] = df["Close"].pct_change()
    return df

def compute_metrics(df: pd.DataFrame) -> dict:
    df = calculate_daily_returns(df)
    avg_return = df["Return"].mean()
    volatility = df["Return"].std()
    return {
        "avg_return": avg_return,
        "volatility": volatility
    }
