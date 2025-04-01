import pika
import json
from dotenv import load_dotenv

from src.infrastructure.infrastructure import Infra
from src.infrastructure.db.database import close_db_connection, cancel_job, db_connection
from src.infrastructure.queue.message_broker import close_broker, start_broker, queue_connection, queue_channel
from src.infrastructure.exchanges.bybit.bybit_exchange import bybit_exchange
from src.infrastructure.logs.log_storage import log_storage

class ConsumerApp(Infra):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.setup_broker()

    def setup_broker(self):
        callback_function = self.generate_callback()
        start_broker(queue_channel, callback_function)

    def generate_callback(self):
        def callback(ch, method, properties, body, order_create_func, market_price_func):
            data = json.loads(body.decode('utf-8'))
            print("Received message:", data)
            try:
                price_limit = data["price_limit"]

                last_price, bid_price, ask_price = bybit_exchange.get_symbol_data(data['symbol'])
                if price_limit and float(last_price) > price_limit:
                    cancel_job(db_connection, data["job_id"])
                    return

                order_data = order_create_func(
                    data["symbol"],
                    data["side"],
                    data["size"],
                    float(bid_price),
                    float(ask_price),
                    price_limit
                )

                market_price = market_price_func(order_data)
                bybit_exchange.make_order(
                    data["symbol"],
                    data["side"],
                    data["size"],
                    market_price
                )
                log_storage.insert_value({
                    "status": "success",
                    "symbol": data["symbol"],
                    "side": data["side"],
                    "size": data["size"],
                    "price": market_price,
                })
            except Exception as e:
                print("Error while placing order:", e)
                cancel_job(db_connection, data["job_id"])
                log_storage.insert_value({
                    "status": "canceled",
                    "symbol": data["symbol"],
                    "side": data["side"],
                })


        return lambda ch, method, properties, body: callback(
            ch,
            method,
            properties,
            body,
            self.manage_order_data.create_order_data,
            self.manage_order_data.get_market_price
        )
