from api.twap_order.manage_twap_order import ManageTwapOrder
from domain.domain import Domain
from api.api import API

class Infra(Domain, API):
    def __init__(self):
        super().__init__(ManageTwapOrder())
