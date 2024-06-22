from alpaca.trading.client import TradingClient
from framework.load_config import load_config

config = load_config('config.yaml')

trading_client = TradingClient(config.alpaca.api_key, config.alpaca.secret_key, paper=True)

def place_order(order):
    # preparing orders
    market_order_data = MarketOrderRequest(
        symbol="SPY",
        qty=0.023,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.DAY
    )

    # Market order
    market_order = trading_client.submit_order(
        order_data=market_order_data
    )


def main():
    account = trading_client.get_account()
    print('connected to account', account)


if __name__ == '__main__':
    main()