# # Clustering / prediction logic

# import pandas as pd
# from sklearn.cluster import KMeans

# def cluster_stocks(features_df: pd.DataFrame, n_clusters: int = 3):
#     model = KMeans(n_clusters=n_clusters, random_state=42)
#     labels = model.fit_predict(features_df)
#     features_df["cluster"] = labels
#     return features_df, model


# modules/ml_engine.py

import pandas as pd
from sklearn.cluster import KMeans

def cluster_stocks(df: pd.DataFrame, n_clusters: int = 3) -> pd.DataFrame:
    """
    Cluster stocks based on numeric features: avg_return and volatility.

    df must contain columns: 'avg_return', 'volatility'
    It may also contain non-numeric columns like 'symbol' – they will be ignored.
    """

    # Work on a copy so we don't modify the original outside
    df = df.copy()

    # Select only numeric features for clustering
    features = df[["avg_return", "volatility"]]

    model = KMeans(n_clusters=n_clusters, random_state=42)
    labels = model.fit_predict(features)

    df["cluster"] = labels
    return df
