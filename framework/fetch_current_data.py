import datetime
import argparse
from fetch_data import fetch_data
from load_config import load_config
import os
import glob

LOOKBACK_DAYS = 30
DATA_FOLDER = 'data'  # directory to store the data files, w.r.t autopilot folder


def fetch_current_data(config_path: str):
    """
    Fetches the data for stock universe defined in the config for last $DATA_AGE days from today and saves the
    data in CSV format in data folder. This method is intended to run every day to fetch the latest data from
    the market, and should be used for calculating weights for portfolio allocation. This method deletes any
    existing data in the 'data' folder and updates it with fresh data
    :param config_path: path to config file
    :return: None
    """
    config = load_config(config_path)
    tickers = config.tickers
    today = datetime.date.today()
    lookback_date = today - datetime.timedelta(days=LOOKBACK_DAYS)

    end_date = today.strftime('%Y-%m-%d')
    start_date = lookback_date.strftime('%Y-%m-%d')
    data = fetch_data(tickers, start_date, end_date)

    check_or_create_folder(DATA_FOLDER)
    delete_csv_files_in_folder(DATA_FOLDER)

    for ticker in tickers:
        ticker_data = data[ticker]
        file_name = os.path.join(DATA_FOLDER, f"{ticker}_{start_date}_{end_date}.csv")
        ticker_data.to_csv(file_name, index=True)

    print(f'Finished downloading data for {len(tickers)} stocks from {start_date} to {end_date}')


def delete_csv_files_in_folder(folder_path):
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
    count = 0
    for file in csv_files:
        try:
            if os.path.isfile(file):
                os.remove(file)  # Delete the file
                count += 1
        except Exception as e:
            print(f"Failed to delete {file}. Reason: {e}")

    print('Deleted {} existing data files'.format(count))


def check_or_create_folder(path):
    """
       Check if a folder exists at the specified path. If it doesn't, create the folder.

       :param path: The path to check or create the folder
       """
    if not os.path.exists(path):
        os.makedirs(path)


def main():
    parser = argparse.ArgumentParser(description='Fetch data for calculating stock weights for portfolio allocation')
    parser.add_argument('--config_path', type=str, default='config.yaml',
                        help='Location of the config file')
    args = parser.parse_args()

    config_path = args.config_path
    fetch_current_data(config_path)


if __name__ == '__main__':
    main()
