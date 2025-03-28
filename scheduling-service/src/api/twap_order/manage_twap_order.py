import datetime
from datetime import datetime
from typing import Tuple, 

from domain.twap_order.twap_order_repository import TwapOrderRepository
rom domain.twap_order.twap_order import TwapOrder

class ManageTwapOrder:
    def __init__(self, twap_order_repository: TwapOrderRepository) -> ManageTwapOrder:
        self.twap_order_repository = twap_order_repository
    
    def create_twap_order(self, symbol: str, side: sideType, total_size: float, total_time: int, frequency: int, price_limit = None) -> TwapOrder:
        return self.twap_order_repository.create_twap_order(symbol, side, total_size, total_time, frequency, price_limit)

    def create_times_for_order(self) -> Tuple[int, datetime]:
        curr_time = datetime.datetime.now()
        duration = self.twap_order_repository.get_duration()
        delay = self.twap_order_repository.get_delay()
        return (delay, curr_time + datetime.timedelta(seconds=duration))



    
