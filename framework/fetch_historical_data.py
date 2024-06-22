import argparse
from load_config import load_config
from fetch_data import fetch_data


def fetch_historical_data(config_path):
    """
    This method is used to fetch stock data for backtesting use cases according to the config file and stored in the
    hdata folder in the format <ticker>_<start_date>_<end_date>.csv
    :param config_path: config file path
    :return: None
    """
    config = load_config(config_path)
    tickers = config.tickers
    start_date = config.backtesting.start_date
    end_date = config.backtesting.end_date
    data = fetch_data(tickers, start_date, end_date)

    for ticker in tickers:
        ticker_data = data[ticker]
        file_name = f"./hdata/{ticker}_{start_date}_{end_date}.csv"
        ticker_data.to_csv(file_name, index=True)

    print(f'Finished downloading data for {len(tickers)} stocks from {start_date} to {end_date}')


def main():
    parser = argparse.ArgumentParser(description='Fetch historical data for backtesting')
    parser.add_argument('--config_path', type=str, default='config.yaml',
                        help='Location of the config file')
    args = parser.parse_args()

    config_path = args.config_path
    fetch_historical_data(config_path)


if __name__ == '__main__':
    main()
