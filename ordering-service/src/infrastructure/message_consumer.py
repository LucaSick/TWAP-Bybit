import pika
import json
from dotenv import load_dotenv

from src.infrastructure.infrastructure import Infra
from src.infrastructure.db.database import database
from src.infrastructure.queue.message_broker import message_broker
from src.infrastructure.exchanges.bybit.bybit_exchange import bybit_exchange
from src.infrastructure.logs.log_storage import log_storage

"""
The consumer application responsible for processing messages from RabbitMQ,
executing orders via an exchange, and logging the outcome.
"""
class ConsumerApp(Infra):
    """
    Loads environment variables and initializes the message broker.
    """
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.setup_broker()

    """
    Starts the RabbitMQ message consumer with a generated callback function.
    """
    def setup_broker(self):
        callback_function = self.generate_callback()
        message_broker.start_broker(callback_function)

    """
    Generates the callback function that will be triggered for every received message.
    This callback:
        - Parses and validates incoming order messages
        - Checks for price limits
        - Creates order data and calculates market price
        - Sends the order to the exchange
        - Logs the result and handles failures
    Returns ->
        Callable: A function with the required pika callback signature.
    """
    def generate_callback(self):
        def callback(ch, method, properties, body, order_create_func, market_price_func):
            data = json.loads(body.decode('utf-8'))
            print("Received message:", data)
            try:
                price_limit = data["price_limit"]

                last_price, bid_price, ask_price = bybit_exchange.get_symbol_data(data['symbol'])
                if price_limit and float(last_price) > price_limit:
                    print("Price limit has been hit, cancelling the job")
                    database.cancel_job(data["job_id"])
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
                database.cancel_job(data["job_id"])
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
