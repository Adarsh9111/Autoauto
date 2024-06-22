import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
warnings.simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
import argparse
from load_data import read_close_price, read_open_price
import numpy as np
import time


'''
Data format for reference:

           MSFT        AAPL       GOOGL        NFLX        META        AMZN
0    101.120003   39.480000   52.734001  267.660004  135.679993   76.956497
1     97.400002   35.547501   51.273499  271.200012  131.740005   75.014000
2    101.930000   37.064999   53.903500  297.570007  137.949997   78.769501
3    102.059998   36.982498   53.796001  315.339996  138.050003   81.475502
4    102.800003   37.687500   54.268501  320.269989  142.529999   82.829002
..          ...         ...         ...         ...         ...         ...
751  334.690002  176.279999  146.916504  614.090027  335.239990  171.068497
752  342.450012  180.330002  147.906494  613.119995  346.179993  169.669495
753  341.250000  179.289993  146.686996  610.710022  346.220001  170.660995
754  341.950012  179.380005  146.654999  610.539978  342.940002  169.201004
755  339.320007  178.199997  146.200500  612.090027  344.359985  168.644501

'''


def mean_reversion_strategy(open_data, close_data, LB):
    """
    Implements mean reversion strategy on given DataFrame for each stock column.

    Parameters:
    - df: DataFrame containing closing prices for each stock.
    - LB: Lookback period for mean reversion calculation.

    Returns:
    - ratio_df: DataFrame with mean reversion ratios for each stock.
    """
    assert LB > 0, "LB must be greater than 0."
    reversion_matrix = calculate_mean_reversion(close_data, LB)

    pnl_per_stock = reversion_matrix * (close_data / open_data - 1)
    pnl = pnl_per_stock.sum(axis=1)
    return pnl


def calculate_mean_reversion(df, LB):
    """
       Calculates the mean reversion matrix for all stocks in the dataframe

       Parameters:
       - df: DataFrame containing closing prices for each stock.
       - LB: Lookback period for mean reversion calculation.

       Returns:
       - ratio_df: DataFrame with mean reversion ratios for each stock.
       """
    # Initialize an empty DataFrame to store mean reversion ratios
    ratio_df = pd.DataFrame(index=df.index, columns=df.columns)

    # Iterate over each column (stock) in the DataFrame
    for col in df.columns:
        # Calculate mean reversion ratio for each day
        for i in range(len(df)):
            if i >= LB:
                # Calculate mean reversion ratio: today's closing price / sum of last LB days' closing prices
                sum_last_LB_days = df.iloc[i - LB: i, df.columns.get_loc(col)].sum()
                yesterday_price = df.iloc[i - 1, df.columns.get_loc(col)]
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

    # return the negative values to imply reversion
    return normalized_means.multiply(-1)


def main():
    start_time = time.time()
    parser = argparse.ArgumentParser(description='Mean reversion strategy')
    parser.add_argument('--verbose', type=bool, default=False, help='Should print vectors?')
    parser.add_argument('--data_path', type=str, default='./data', help="Path to the folder with csv data")
    parser.add_argument('--lookback', type=int, default=5, help="Days to lookback when calculating reversion")
    args = parser.parse_args()

    data_path = args.data_path
    verbose = args.verbose
    LB = args.lookback
    close_data = read_close_price(data_path)
    open_data = read_open_price(data_path)

    # Apply mean reversion strategy
    mean_reversion_values = mean_reversion_strategy(open_data, close_data, LB)

    # Print mean reversion values
    if verbose:
        print("Mean reversion strategy")
        print("-- lookback:", LB)
        print("-- universe size:", len(close_data.columns))
        print("-- trading days:", len(close_data))
        print("\nPnL vector (in bps): ")
        print(mean_reversion_values)
    print("\n--- Aggregate PnL for all stocks over trading duration (in bps): ", mean_reversion_values.sum(axis=0))
    print("--- Executed in %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
