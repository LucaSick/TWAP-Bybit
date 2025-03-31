from src.domain.order_data.order_data_repository import OrderDataRepository

class Domain:
    def __init__(self, order_data_repository: OrderDataRepository):
        self.order_data_repository = order_data_repository
