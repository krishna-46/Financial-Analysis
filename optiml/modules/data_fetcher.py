# Yahoo Finance / API functions

import yfinance as yf
import pandas as pd

def get_stock_history(symbol: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period, interval=interval)
    hist.reset_index(inplace=True)
    return hist

def get_stock_info(symbol: str) -> dict:
    ticker = yf.Ticker(symbol)
    info = ticker.info  # may be .get_info() in newer versions
    return info
