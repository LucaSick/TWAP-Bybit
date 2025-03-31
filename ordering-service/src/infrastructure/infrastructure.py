from src.api.order_data.manage_order_data import ManageOrderData
from src.domain.domain import Domain
from src.api.api import API
from src.domain.order_data.order_data_repository import OrderDataRepository

class Infra(API):
    def __init__(self):
        super().__init__(ManageOrderData(OrderDataRepository()))
