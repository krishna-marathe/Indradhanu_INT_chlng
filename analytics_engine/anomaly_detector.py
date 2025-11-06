import pandas as pd
import numpy as np

def detect_anomalies(df, column, threshold=2.5):
    """Detects anomalies in numeric column using z-score."""
    if column not in df.columns:
        return []
    df = df.copy()
    df['zscore'] = (df[column] - df[column].mean()) / df[column].std()
    anomalies = df[np.abs(df['zscore']) > threshold]
    return anomalies[[column, 'zscore']].to_dict(orient='records')