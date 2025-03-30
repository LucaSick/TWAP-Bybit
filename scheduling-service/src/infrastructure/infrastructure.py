from src.api.twap_order.manage_twap_order import ManageTwapOrder
from src.domain.domain import Domain
from src.api.api import API
from src.domain.twap_order.twap_order_repository import TwapOrderRepository

class Infra(API):
    def __init__(self):
        super().__init__(ManageTwapOrder(TwapOrderRepository()))
