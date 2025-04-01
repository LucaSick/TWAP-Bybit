from pybit.unified_trading import HTTP
import os

from src.infrastructure.exchanges.exchange_interface import ExchangeInterface

class BybitExchange(ExchangeInterface):
    def __init__(self):
        self.session = HTTP(
            testnet=True,
            api_key=os.getenv("BYBIT_API_KEY"),
            api_secret=os.getenv("BYBIT_API_SECRET")
        )

    def get_symbol_data(self, symbol):
        print("Getting ticker data for", symbol)
        ticker_response = self.session.get_tickers(
            category="linear",
            symbol=symbol,
        )
        result = ticker_response["result"]["list"][0]
        print("Symbol data:", result)
        return result["lastPrice"], result["bid1Price"], result["ask1Price"]

    def make_order(self, symbol, side, size, price):
        print("Placing order for", symbol)
        bybitSide = "Buy" if side == "bid" else "Sell"
        self.session.place_order(
            category="linear",
            symbol=symbol,
            side=bybitSide,
            orderType="Limit",
            qty=size,
            price=round(price, 4),
        )
        print("Order placed:", symbol, side, size, price)

bybit_exchange = BybitExchange()
