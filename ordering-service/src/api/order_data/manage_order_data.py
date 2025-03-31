import datetime
from datetime import datetime, timedelta
from typing import Tuple

from src.domain.order_data.order_data_repository import OrderDataRepository
from src.domain.order_data.order_data import OrderData
from src.constants.order import sideType

class ManageOrderData:
    def __init__(self, order_data_repository: OrderDataRepository):
        self.order_data_repository = order_data_repository
    
    def create_order_data(self, symbol: str, side: sideType, size: float, bid_price: float, ask_price: float, price_limit: float | None = None):
        return self.order_data_repository.create_order_data(symbol, side, size, bid_price, ask_price, price_limit)

    def get_market_price(self, order_data: OrderData):
        bid_price = self.order_data_repository.get_best_bid_price(order_data)
        ask_price = self.order_data_repository.get_best_ask_price(order_data)
        return (bid_price + ask_price) / 2



    
