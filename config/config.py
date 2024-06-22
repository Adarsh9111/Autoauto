import yaml


class Backtesting:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date


class Config:
    def __init__(self, tickers, backtesting):
        self.tickers = tickers
        self.backtesting = Backtesting(**backtesting)


def read_config(file_path):
    with open(file_path, 'r') as f:
        config_dict = yaml.safe_load(f)
    config = Config(**config_dict)
    return config


if __name__ == '__main__':
    config = read_config('./config/config.yaml')
    print("Read config tickers", config.tickers)
    print("Read config backtesting", config.backtesting.start_date, config.backtesting.end_date)
