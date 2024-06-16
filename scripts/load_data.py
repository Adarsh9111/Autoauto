import os
import pandas as pd


def read_stock_data(folder_path: str):
    """
    Function to read multiple CSV files from a folder and combine them into a single DataFrame.
    
    Parameters:
    - folder_path (str): Path to the folder containing CSV files
    
    Returns:
    - DataFrame: Combined DataFrame where each stock's data can be accessed using df['ticker']
    """
    combined_df = pd.DataFrame()
    ticker_data = {}

    # List all files in the folder
    files = os.listdir(folder_path)

    # Iterate over each file
    for file in files:
        if file.endswith('.csv'):
            # Extract ticker and dates from filename (assuming filename is ticker_start_date_end_date.csv)
            file_parts = os.path.splitext(file)[0].split('_')
            ticker = file_parts[0]
            start_date = file_parts[1]
            end_date = file_parts[2]

            # Read CSV file into DataFrame
            file_path = os.path.join(folder_path, file)
            df = pd.read_csv(file_path)

            # Store data in a dictionary by ticker symbol
            if ticker not in ticker_data:
                ticker_data[ticker] = df
            else:
                # Assuming you want to concatenate data if multiple files exist for the same ticker
                ticker_data[ticker] = pd.concat([ticker_data[ticker], df], ignore_index=True)

    # Create combined DataFrame
    combined_df = pd.concat(ticker_data.values(), axis=1, keys=ticker_data.keys())

    return combined_df


def read_close_price(folder_path: str):
    """
    Create a new DataFrame with closing prices for each stock.

    Parameters:
    - combined_df (DataFrame): DataFrame containing combined stock data with MultiIndex columns.

    Returns:
    - DataFrame: DataFrame with columns as tickers and rows as closing prices for each stock on each date.
    """
    data = read_stock_data(folder_path)
    # Initialize an empty DataFrame with Date index
    closing_prices_df = pd.DataFrame(index=data.index.get_level_values(0).unique())

    # Populate closing prices for each ticker
    for ticker in data.columns.levels[0]:
        close_col = (ticker, 'Close')
        closing_prices_df[ticker] = data[close_col]

    return closing_prices_df


def main():
    # Example usage:
    folder_path = './data'
    combined_data = read_stock_data(folder_path)

    # Access data for a specific ticker
    ticker_data = combined_data['AAPL']

    # Print combined DataFrame
    print(combined_data)

    # Print data for a specific ticker (e.g., AAPL)
    print(ticker_data)


if __name__ == '__main__':
    main()
