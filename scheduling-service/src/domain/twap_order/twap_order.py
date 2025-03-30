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
    
    def get_total_orders(self):
        return self.total_time / self.frequency
    
    def get_size_per_order(self):
        return self.total_size / self.get_total_orders()
    
    def get_symbol(self):
        return self.symbol
    
    def get_side(self):
        return self.side
    
    def get_price_limit(self):
        return self.price_limit
    
    def get_delay(self):
        return self.frequency
    
    def get_duration(self):
        return self.total_time