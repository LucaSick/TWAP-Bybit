from src.domain.order_data.order_data import OrderData
from src.constants.order import sideType

"""
Repository for creating and accessing data of trading orders.
"""
class OrderDataRepository:
    """
    Constructs an OrderData instance with the given trading information.
    Args ->
        symbol (str): The trading symbol (e.g., 'BTC/USDT').
        side (sideType): The side of the order ('bid' or 'ask').
        size (float): Quantity to trade.
        bid_price (float): Current market bid price.
        ask_price (float): Current market ask price.
        price_limit (float | None): Optional maximum price limit.
    Returns ->
        OrderData: A new OrderData instance.
    """
    def create_order_data(self, symbol: str, side: sideType, size: float, bid_price: float, ask_price: float, price_limit: float | None = None):
        return OrderData(symbol, side, size, bid_price, ask_price, price_limit)

    """
    Retrieves the current best bid price from the order data.
    Args -> order_data (OrderData): The order data instance.
    Returns -> float: The current best bid price.
    """
    def get_best_bid_price(self, order_data: OrderData):
        return order_data.bid_price

    """
    Retrieves the current best ask price from the order data.
    Args -> order_data (OrderData): The order data instance.
    Returns -> float: The current best ask price.
    """
    def get_best_ask_price(self, order_data: OrderData):
        return order_data.ask_price