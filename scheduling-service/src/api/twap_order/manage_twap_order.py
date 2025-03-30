import datetime
from datetime import datetime, timedelta
from typing import Tuple

from src.domain.twap_order.twap_order_repository import TwapOrderRepository
from src.domain.twap_order.twap_order import TwapOrder
from src.constants.twap import sideType

class ManageTwapOrder:
    def __init__(self, twap_order_repository: TwapOrderRepository):
        self.twap_order_repository = twap_order_repository
    
    def create_twap_order(self, symbol: str, side: sideType, total_size: float, total_time: int, frequency: int, price_limit: float | None = None) -> TwapOrder:
        return self.twap_order_repository.create_twap_order(symbol, side, total_size, total_time, frequency, price_limit)

    def create_times_for_order(self, twap_order: TwapOrder) -> Tuple[int, datetime]:
        curr_time = datetime.now()
        duration = self.twap_order_repository.get_duration(twap_order)
        delay = self.twap_order_repository.get_delay(twap_order)
        return (delay, curr_time + timedelta(seconds=duration))



    
