from src.domain.order_data.order_data import OrderData
from src.constants.order import sideType

class OrderDataRepository:
    def create_order_data(self, symbol: str, side: sideType, size: float, bid_price: float, ask_price: float, price_limit: float | None = None):
        return OrderData(symbol, side, size, bid_price, ask_price, price_limit)
    
    def get_best_bid_price(self, order_data: OrderData):
        return order_data.bid_price

    def get_best_ask_price(self, order_data: OrderData):
        return order_data.ask_price