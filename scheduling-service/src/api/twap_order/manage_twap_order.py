import datetime
from datetime import datetime, timedelta
from typing import Tuple

from src.domain.twap_order.twap_order_repository import TwapOrderRepository
from src.domain.twap_order.twap_order import TwapOrder
from src.constants.twap import sideType

"""
Service layer responsible for managing TWAP orders.
"""
class ManageTwapOrder:
    """
    Initializes the manager with a TWAP order repository.
    Args -> twap_order_repository (TwapOrderRepository): The repository used for TWAP order operations.
    """
    def __init__(self, twap_order_repository: TwapOrderRepository):
        self.twap_order_repository = twap_order_repository
    
    """
    Creates and returns a new TWAP order using the repository.
    Args ->
        symbol (str): Trading symbol.
        side (sideType): Buy or sell side.
        total_size (float): Total size to trade.
        total_time (int): Duration in seconds.
        frequency (int): Delay between each sub-order.
        price_limit (float | None): Optional price cap to enforce.
    Returns -> TwapOrder: The created TWAP order instance.
    """
    def create_twap_order(self, symbol: str, side: sideType, total_size: float, total_time: int, frequency: int, price_limit: float | None = None) -> TwapOrder:
        return self.twap_order_repository.create_twap_order(symbol, side, total_size, total_time, frequency, price_limit)

    """
    Calculates the delay between executions and the end time of the order.
    Args -> twap_order (TwapOrder): The TWAP order instance.
    Returns ->
        Tuple[int, datetime]: A tuple containing:
            - Delay in seconds between executions.
            - The calculated end time as a datetime object.
    """
    def create_times_for_order(self, twap_order: TwapOrder) -> Tuple[int, datetime]:
        curr_time = datetime.now()
        duration = self.twap_order_repository.get_duration(twap_order)
        delay = self.twap_order_repository.get_delay(twap_order)
        return (delay, curr_time + timedelta(seconds=duration))
