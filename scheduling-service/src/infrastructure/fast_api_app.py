from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
import time


from src.domain.domain import Domain
from src.api.api import API
from src.infrastructure.infrastructure import Infra
from src.constants.twap import sideType
from src.infrastructure.db.database import setup_database
from src.infrastructure.scheduler.scheduler import setup_sched, shutdown_scheduler, add_job, create_scheduler
from src.infrastructure.queue.message_broker import send_message, close_broker, queue_connection, queue_channel

def send_order(symbol, side, size, price_limit):
    body = {
        "symbol": symbol,
        "side": side,
        "size": size,
        "price_limit": price_limit,
    }
    send_message(queue_channel, body)

class TwapOrderBody(BaseModel):
    symbol: str
    side: sideType
    total_size: float
    total_time: int
    frequency: int
    price_limit: float | None = None

class SchedulingService(Infra):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.app = FastAPI()
        self.setup_db()
        self.setup_scheduler()
        self.setup_routes()
    
    def setup_db(self):
        conn, cur = setup_database()
        self.conn = conn
        self.cur = cur

    def setup_scheduler(self):
        self.scheduler = create_scheduler()
    
    def setup_routes(self):
        @self.app.get("/status")
        def get_status():
            return {"status": "ok"}

        @self.app.post("/twap-strategy")
        def twap_strategy(body: TwapOrderBody):
            order = self.manage_twap_order.create_twap_order(body.symbol, body.side, body.total_size, body.total_time, body.frequency, body.price_limit)
            delay, end_datetime = self.manage_twap_order.create_times_for_order(order)
            add_job(self.scheduler, send_order, delay, end_datetime, [order.get_symbol(), order.get_side(), order.get_size_per_order(), order.get_price_limit()])
            return {"status": "done", "delay": delay, "end_date": end_datetime, "size": order.get_size_per_order()}
        
        @self.app.on_event("shutdown")
        def shutdown_event():
            shutdown_scheduler(self.scheduler)
            close_broker(queue_connection)
