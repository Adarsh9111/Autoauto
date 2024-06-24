import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_weights(df):
    """
    This function normalizes the dataframe to get the weights for each stock.]

    This Function should always be applied on top of an alpha
    """
    delay = 1
    delay_df = df.shift(delay)

    mean_per_date = delay_df.mean(axis=1)
    normalized_df = delay_df.sub(mean_per_date, axis=0)
    abs_sum_per_date = normalized_df.abs().sum(axis=1)
    weights = normalized_df.div(abs_sum_per_date, axis=0)

    return weights

def calculate_daily_returns(prices):
    """
    This function calculates daily returns from the closing price data.
    """
    returns = prices.pct_change().fillna(0)
    return returns

def calculate_pnl(prices, data):
    """
    This function calculates the PnL for the strategy.
    
    prices: DataFrame with closing stock prices.
    data: DataFrame with the data used to calculate weights (e.g., historical prices or indicators).
    """
    weights = calculate_weights(data)
    returns = calculate_daily_returns(prices)
    
    # Align the lengths of weights and returns
    weights = weights.iloc[1:]
    returns = returns.iloc[1:]
    
    # Calculate daily PnL matrix
    daily_pnl_matrix = weights * returns
    
    return daily_pnl_matrix

def calculate_total_pnl(pnl_matrix):
    """
    This function calculates the total PnL.
    
    pnl_matrix: DataFrame with daily PnL values for each stock.
    """
    total_pnl = pnl_matrix.sum().sum()
    return total_pnl

def calculate_annual_pnl(pnl_matrix):
    """
    This function calculates the annual PnL.
    
    pnl_matrix: DataFrame with daily PnL values for each stock.
    """
    # Assuming 252 trading days in a year
    daily_pnl = pnl_matrix.sum(axis=1)
    annual_pnl = daily_pnl.mean() * 252
    return annual_pnl

def plot_cumulative_pnl(pnl_matrix):
    """
    This function plots the cumulative PnL vs days.
    
    pnl_matrix: DataFrame with daily PnL values for each stock.
    """
    daily_pnl = pnl_matrix.sum(axis=1)
    cumulative_pnl = daily_pnl.cumsum()
    plt.figure(figsize=(12, 6))
    plt.plot(cumulative_pnl, label='Cumulative PnL')
    plt.xlabel('Date')
    plt.ylabel('Cumulative PnL')
    plt.title('Cumulative PnL vs Days')
    plt.legend()
    plt.grid(True)
    plt.show()