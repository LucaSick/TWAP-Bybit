from src.constants.order import sideType

"""
Represents a trading order's essential data
Attributes ->
    symbol (str): The trading pair symbol (e.g., 'BTC/USDT').
    side (sideType): Indicates whether the order is a 'bid' (buy) or 'ask' (sell).
    size (float): The quantity of the asset to trade.
    bid_price (float): The current bid price in the market.
    ask_price (float): The current ask price in the market.
    price_limit (float | None): Optional price constraint that should not be exceeded.
"""
class OrderData:
    def __init__(self, symbol: str, side: sideType, size: float, bid_price: float, ask_price: float, price_limit: float | None = None):
        self.symbol = symbol
        self.side = side
        self.size = size
        self.price_limit = price_limit
        self.bid_price = bid_price
        self.ask_price = ask_price
