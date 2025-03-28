from domain.twap_order.twap_order_repository import TwapOrderRepository
from api.twap_order.manage_twap_order import ManageTwapOrder
from domain.domain import Domain

class API(Domain):
    def __init__(self, manage_twap_order: ManageTwapOrder):
        super().__init__(TwapOrderRepository())
        self.manage_twap_order = manage_twap_order

    
