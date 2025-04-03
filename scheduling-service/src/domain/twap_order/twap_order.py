from src.constants.twap import sideType

class TwapOrder:
    """
    Represents a TWAP order.

    Attributes:
        symbol (str): The trading symbol (e.g., 'BTC/USDT') to be bought or sold.
        side (sideType): The side of the trade, either 'bid' (buy) or 'ask' (sell).
        total_size (float): The total quantity of the asset to trade.
        total_time (int): The total duration over which the order should be executed, in seconds.
        frequency (int): The time interval (in seconds) between each order execution.
        price_limit (float | None): Optional upper/lower price limit. If the market price exceeds this limit, 
                                    the TWAP execution will be terminated.
    """
    def __init__(self, symbol: str, side: sideType, total_size: float, total_time: int, frequency: int, price_limit: float | None = None):
        self.symbol = symbol
        self.side = side
        self.total_size = total_size
        self.total_time = total_time
        self.frequency = frequency
        self.price_limit = price_limit
