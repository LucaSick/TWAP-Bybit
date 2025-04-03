import datetime
from datetime import datetime, timedelta
from typing import Tuple

from src.domain.order_data.order_data_repository import OrderDataRepository
from src.domain.order_data.order_data import OrderData
from src.constants.order import sideType

"""
Service layer responsible for managing and processing OrderData logic.
"""
class ManageOrderData:
    """
    Initializes the manager with an OrderDataRepository instance.
    Args -> order_data_repository (OrderDataRepository): Repository used to access order data.
    """
    def __init__(self, order_data_repository: OrderDataRepository):
        self.order_data_repository = order_data_repository

    """
    Creates a new OrderData instance via the repository.
    Args ->
        symbol (str): The trading symbol.
        side (sideType): Order side ('bid' or 'ask').
        size (float): Quantity to trade.
        bid_price (float): Current bid price.
        ask_price (float): Current ask price.
        price_limit (float | None): Optional price constraint.
    Returns -> OrderData: The constructed order data object.
    """
    def create_order_data(self, symbol: str, side: sideType, size: float, bid_price: float, ask_price: float, price_limit: float | None = None):
        return self.order_data_repository.create_order_data(symbol, side, size, bid_price, ask_price, price_limit)

    """
    Calculates the mid-market price from the best bid and ask.
    Args -> order_data (OrderData): The order data instance.
    Returns -> float: The average of the best bid and ask prices.
    """
    def get_market_price(self, order_data: OrderData):
        bid_price = self.order_data_repository.get_best_bid_price(order_data)
        ask_price = self.order_data_repository.get_best_ask_price(order_data)
        return (bid_price + ask_price) / 2
