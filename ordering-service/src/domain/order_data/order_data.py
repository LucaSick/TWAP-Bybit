# TODO: Document code
from src.constants.order import sideType

class OrderData:
    def __init__(self, symbol: str, side: sideType, size: float, bid_price: float, ask_price: float, price_limit: float | None = None):
        self.symbol = symbol
        self.side = side
        self.size = size
        self.price_limit = price_limit
        self.bid_price = bid_price
        self.ask_price = ask_price
