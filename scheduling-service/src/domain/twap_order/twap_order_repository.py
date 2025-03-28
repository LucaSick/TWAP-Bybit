from twar_order import TwapOrder

class TwapOrderRepository:
    def create_twap_order(symbol: str, side: sideType, total_size: float, total_time: int, frequency: int, price_limit = None):
        return TwapOrder(symbol, side, total_size, total_time, frequency, price_limit)

    def get_total_orders(order: TwapOrder):
        return order.total_time / order.frequency
    
    def get_price_per_order(order: TwapOrder):
        return order.total_size / self.get_price_per_order(order)
    
    def get_delay(order: TwapOrder):
        return order.frequency
    
    def get_duration(order: TwapOrder):
        return order.total_time