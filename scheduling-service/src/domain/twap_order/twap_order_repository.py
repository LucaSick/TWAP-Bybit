from src.domain.twap_order.twap_order import TwapOrder
from src.constants.twap import sideType

"""
Repository for managing and retrieving data from TWAP orders.
"""
class TwapOrderRepository:
    """
    Instantiates a new TwapOrder object with the provided parameters.
    Args ->
        symbol (str): The trading symbol.
        side (sideType): The side of the order.
        total_size (float): Total quantity to be traded.
        total_time (int): Duration over which the order is executed (in seconds).
        frequency (int): Interval between each trade execution (in seconds).
        price_limit (float | None): Optional price limit that will terminate the order if exceeded.
    Returns -> TwapOrder: The created TWAP order instance.
    """
    def create_twap_order(self, symbol: str, side: sideType, total_size: float, total_time: int, frequency: int, price_limit: float | None = None):
        return TwapOrder(symbol, side, total_size, total_time, frequency, price_limit)

    """
    Calculates the number of sub-orders based on the total time and frequency.
    Args -> order (TwapOrder): The TWAP order instance.
    Returns -> float: Total number of sub-orders to be executed.
    """
    def get_total_orders(self, order: TwapOrder):
        return order.total_time / order.frequency

    """
    Calculates the quantity of asset to trade per sub-order.
    Args -> order (TwapOrder): The TWAP order instance.
    Returns -> float: Quantity per sub-order.
    """
    def get_size_per_order(self, order: TwapOrder):
        return order.total_size / self.get_total_orders(order)

    """
    Retrieves the delay (interval) between each trade execution.
    Args -> order (TwapOrder): The TWAP order instance.
    Returns -> int: Delay in seconds.
    """
    def get_delay(self, order: TwapOrder):
        return order.frequency
    
    """
    Retrieves the total duration of the TWAP order.
    Args -> order (TwapOrder): The TWAP order instance.
    Returns -> int: Duration in seconds.
    """
    def get_duration(self, order: TwapOrder):
        return order.total_time

    """
    Retrieves the trading symbol of the order.
    Args -> order (TwapOrder): The TWAP order instance.
    Returns -> str: Trading symbol.
    """
    def get_symbol(self, order: TwapOrder):
        return order.symbol

    """
    Retrieves the side (buy/sell) of the order.
    Args -> order (TwapOrder): The TWAP order instance.
    Returns -> sideType: 'bid' or 'ask'.
    """
    def get_side(self, order: TwapOrder):
        return order.side

    """
    Retrieves the optional price limit of the order.
    Args -> order (TwapOrder): The TWAP order instance.
    Returns -> float | None: Price limit, or None if not set.
    """
    def get_price_limit(self, order: TwapOrder):
        return order.price_limit