from src.domain.twap_order.twap_order import TwapOrder
from src.constants.twap import sideType

class TwapOrderRepository:
    def create_twap_order(self, symbol: str, side: sideType, total_size: float, total_time: int, frequency: int, price_limit: float | None = None):
        return TwapOrder(symbol, side, total_size, total_time, frequency, price_limit)

    def get_total_orders(self, order: TwapOrder):
        return order.total_time / order.frequency
    
    def get_size_per_order(self, order: TwapOrder):
        return order.total_size / self.get_total_orders(order)
    
    def get_delay(self, order: TwapOrder):
        return order.frequency
    
    def get_duration(self, order: TwapOrder):
        return order.total_time
    
    def get_symbol(self, order: TwapOrder):
        return order.symbol
    
    def get_side(self, order: TwapOrder):
        return order.side
    
    def get_price_limit(self, order: TwapOrder):
        return order.price_limit