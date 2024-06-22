import yfinance as yf

THREAD_COUNT = 4


def fetch_data(tickers: list[str], start_date: str, end_date: str):
    """
    Fetch data from Yahoo finance for the list of tickers and the time range specified in the arguments.

    :param tickers: list of tickers to fetch data from
    :param start_date: start date of data to be fetched
    :param end_date: end date of data to be fetched
    :return: dictionary of dataframes with keys as tickers, e.g. access Apple data using df['AAPL']
    """
    combined_tickers = " ".join(tickers)
    data = yf.download(combined_tickers, start=start_date, end=end_date, group_by='ticker', threads=THREAD_COUNT)
    return data
