# TODO: Document code
from src.constants.twap import sideType

class TwapOrder:
    def __init__(self, symbol: str, side: sideType, total_size: float, total_time: int, frequency: int, price_limit: float | None = None):
        self.symbol = symbol
        self.side = side
        self.total_size = total_size
        self.total_time = total_time
        self.frequency = frequency
        self.price_limit = price_limit
