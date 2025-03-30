from src.domain.twap_order.twap_order_repository import TwapOrderRepository

class Domain:
    def __init__(self, twap_order_repository: TwapOrderRepository):
        self.twap_order_repository = twap_order_repository
