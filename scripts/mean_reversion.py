import pandas as pd
from load_data import read_close_price
import numpy as np


def mean_reversion_strategy(df, LB):
    """
    Implements mean reversion strategy on given DataFrame for each stock column.

    Parameters:
    - df: DataFrame containing closing prices for each stock.
    - LB: Lookback period for mean reversion calculation.

    Returns:
    - ratio_df: DataFrame with mean reversion ratios for each stock.
    """
    assert LB > 0, "LB must be greater than 0."
    # Initialize an empty DataFrame to store mean reversion ratios
    ratio_df = pd.DataFrame(index=df.index, columns=df.columns)

    # Iterate over each column (stock) in the DataFrame
    for col in df.columns:
        # Calculate mean reversion ratio for each day
        for i in range(len(df)):
            if i >= LB:
                # Calculate mean reversion ratio: today's closing price / sum of last LB days' closing prices
                sum_last_LB_days = df.iloc[i - LB: i, df.columns.get_loc(col)].sum()
                yesterday_price = df.iloc[i-1, df.columns.get_loc(col)]
                mean_reversion_ratio = yesterday_price / sum_last_LB_days
                ratio_df.at[df.index[i], col] = mean_reversion_ratio
            else:
                # For the first LB days, cannot calculate mean reversion ratio, so set as NaN
                ratio_df.at[df.index[i], col] = float('NaN')

    # subtract all elements with the mean
    day_mean = ratio_df.mean(axis=1)
    adjusted_means = ratio_df.subtract(day_mean, axis=0)

    # normalize the values
    sums = adjusted_means.abs().sum(axis=1).replace(0, np.nan)
    normalized_means = adjusted_means.divide(sums, axis=0)

    return normalized_means


def main():
    data_path = './data'
    stock_data = read_close_price(data_path)

    LB = 5  # Lookback period

    # Apply mean reversion strategy
    mean_reversion_values = mean_reversion_strategy(stock_data, LB)

    # Print mean reversion values
    print("Mean Reversion Values:")
    print(mean_reversion_values)


if __name__ == '__main__':
    main()
