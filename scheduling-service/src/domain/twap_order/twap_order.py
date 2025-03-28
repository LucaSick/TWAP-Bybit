# TODO: Document code
from constants.twap import sideType

class TwapOrder:
    def __init__(self, symbol: str, side: sideType, total_size: float, total_time: int, frequency: int, price_limit = None):
        self.symbol = symbol
        self.side = side
        self.total_size = total_size
        self.total_time = total_time
        self.frequency = frequency
        self.price_limit = price_limit
    
    def get_total_orders(self):
        return self.total_time / self.frequency
    
    def get_price_per_order(self):
        return self.total_size / self.get_price_per_order()
    
    def get_delay(self):
        return self.frequency
    
    def get_duration(self):
        return self.total_time