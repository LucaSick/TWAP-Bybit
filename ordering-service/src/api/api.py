from src.domain.order_data.order_data_repository import OrderDataRepository
from src.api.order_data.manage_order_data import ManageOrderData
from src.domain.domain import Domain

class API(Domain):
    def __init__(self, manage_order_data: ManageOrderData):
        super().__init__(manage_order_data.order_data_repository)
        self.manage_order_data = manage_order_data
