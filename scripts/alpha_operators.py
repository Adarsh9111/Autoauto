import pandas as pd
import numpy as np

def add(df1, df2, filter=False):
    if filter:
        df1 = df1.fillna(0)
        df2 = df2.fillna(0)
    return df1 + df2

def divide(df1, df2):
    return df1 / df2

def reverse(df):
    return -df

def inverse(df):
    return 1 / df

def multiply(*dfs, filter=True):
    result = dfs[0].copy()
    for df in dfs[1:]:
        if filter:
            df = df.fillna(1)
        result *= df
    if filter:
        result = result.replace(1, np.nan)
    return result

def ts_rank(df, d):
    def rank_series(s):
        return pd.Series(s).rank().iloc[-1] / len(s)
    return df.rolling(window=d).apply(rank_series, raw=False)

def rank(df):
    return df.rank(axis=1, pct=True)

def normalize(df):
    mean_per_date = df.mean(axis=1)
    df = df.sub(mean_per_date, axis=0)
    abs_sum_per_date = df.abs().sum(axis=1)
    return df.div(abs_sum_per_date, axis=0)