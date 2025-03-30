from src.domain.twap_order.twap_order_repository import TwapOrderRepository
from src.api.twap_order.manage_twap_order import ManageTwapOrder
from src.domain.domain import Domain

class API(Domain):
    def __init__(self, manage_twap_order: ManageTwapOrder):
        super().__init__(manage_twap_order.twap_order_repository)
        self.manage_twap_order = manage_twap_order

    
