from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
import time


from src.domain.domain import Domain
from src.api.api import API
from src.infrastructure.infrastructure import Infra
from src.constants.twap import sideType
from src.infrastructure.db.database import database
from src.infrastructure.scheduler.scheduler import scheduler
from src.infrastructure.queue.message_broker import message_broker

"""
Called on each interval to send a order message to the broker unless the job is canceled.
Args ->
    symbol (str): Trading pair symbol.
    side (sideType): Order side ("bid" or "ask").
    size (float): Size per order.
    price_limit (float | None): Optional price limit.
    job_id (str): The job's unique identifier.
"""
def send_order(symbol, side, size, price_limit, job_id):
    canceled = database.is_canceled(job_id)
    if canceled:
        scheduler.remove_job(job_id)
        print(f"Job {job_id} cancelled.")
        return

    body = {
        "symbol": symbol,
        "side": side,
        "size": size,
        "price_limit": price_limit,
        "job_id": job_id,
    }
    message_broker.send_message(body)

"""
Request schema for scheduling a TWAP strategy.
"""
class TwapOrderBody(BaseModel):
    symbol: str
    side: sideType
    total_size: float
    total_time: int
    frequency: int
    price_limit: float | None = None

"""
FastAPI service for scheduling and managing TWAP strategies.
"""
class SchedulingService(Infra):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.app = FastAPI()
        scheduler.setup_scheduler()
        self.setup_routes()

    """
    Registers API routes for the TWAP scheduling service.
    """
    def setup_routes(self):
        """
        Health check endpoint.
        """
        @self.app.get("/status")
        def get_status():
            return {"status": "ok"}

        """
        Endpoint to schedule a TWAP strategy.
        """
        @self.app.post("/twap-strategy")
        def twap_strategy(body: TwapOrderBody):
            order = self.manage_twap_order.create_twap_order(body.symbol, body.side, body.total_size, body.total_time, body.frequency, body.price_limit)
            delay, end_datetime = self.manage_twap_order.create_times_for_order(order)
            params = {
                "symbol": self.twap_order_repository.get_symbol(order),
                "side": self.twap_order_repository.get_side(order), 
                "size": self.twap_order_repository.get_size_per_order(order), 
                "price_limit": self.twap_order_repository.get_price_limit(order)
            }
            job_info = scheduler.add_job(send_order, delay, end_datetime, params)
            database.add_job_to_db(job_info)
            return {
                "status": "scheduled",
                "delay": delay,
                "end_date": end_datetime,
                "size": self.twap_order_repository.get_size_per_order(order)
            }
        
        """
        Cleanup resources on application shutdown.
        """
        @self.app.on_event("shutdown")
        def shutdown_event():
            scheduler.shutdown_scheduler()
            message_broker.close_broker()
            database.close_db_connection()
