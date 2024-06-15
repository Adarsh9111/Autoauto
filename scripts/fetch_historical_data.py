import yfinance as yf
import argparse
import csv
import pandas as pd

AUTO_FETCH_TICKER = 'AUTO_FETCH_TICKER'

def fetch_historical_data(ticker_list: str, start_date: str, end_date: str):
    tickers = []
    if ticker_list == AUTO_FETCH_TICKER:
        raw_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
        tickers = raw_tickers.Symbol.tolist()
    else:
        with open(ticker_list, mode='r', newline='') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader) # ignore the headers
            data = [row for row in csv_reader]
            for row in data:
                tickers.append(row[0])

    combined_tickers = " ".join(tickers)

    data = yf.download(combined_tickers, start=start_date, end=end_date, group_by='ticker', threads=4)
    
    for ticker in tickers:
        ticker_data = data[ticker]
        file_name = f"./data/{ticker}_{start_date}_{end_date}.csv"
        print('file_name: ', file_name)
        ticker_data.to_csv(file_name, index=True)

def main():
    parser = argparse.ArgumentParser(description='Process CSV file URI.')
    parser.add_argument('--csv_uri', type=str, default=AUTO_FETCH_TICKER, help='The URI of the CSV file (default: default.csv)')
    parser.add_argument('start_date', type=str, help='The start date in YYYY-MM-DD format')
    parser.add_argument('end_date', type=str, help='The end date in YYYY-MM-DD format')
    args = parser.parse_args()

    csv_uri = args.csv_uri
    start_date = args.start_date
    end_date = args.end_date

    fetch_historical_data(csv_uri, start_date, end_date)

if __name__ == '__main__':
    main()