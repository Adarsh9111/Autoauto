import yaml


class Backtesting:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date


class Alpaca:
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key


class Config:
    def __init__(self, tickers, backtesting, alpaca):
        self.tickers = tickers
        self.backtesting = Backtesting(**backtesting)
        self.alpaca = Alpaca(**alpaca)


def load_config(file_path):
    """
    Load configuration from the config YAML file
    :param file_path: path to config file
    :return: config object
    """
    with open(file_path, 'r') as f:
        config_dict = yaml.safe_load(f)
    config = Config(**config_dict)
    return config


if __name__ == '__main__':
    config = load_config('./config/config.yaml')
    print("Read config tickers", config.tickers)
    print("Read config backtesting", config.backtesting.start_date, config.backtesting.end_date)
