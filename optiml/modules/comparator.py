# modules/comparator.py

from .analytics import compute_metrics

def compare_two(df1, df2, s1: str, s2: str) -> dict:
    """
    Compare two stocks based on basic metrics like
    average return and volatility.

    df1, df2 : price history DataFrames (must have Close column)
    s1, s2   : stock symbols (strings)
    """
    m1 = compute_metrics(df1)
    m2 = compute_metrics(df2)

    comparison = {
        "stocks": [s1, s2],
        "metrics": {
            s1: m1,
            s2: m2,
        },
        "better_return": s1 if m1["avg_return"] > m2["avg_return"] else s2,
        "lower_risk": s1 if m1["volatility"] < m2["volatility"] else s2,
    }

    return comparison
