import pika
import os
import time


"""
Handles connection to RabbitMQ and provides functionality to consume messages.
"""
class MessageBroker:
    """
    Initializes the MessageBroker instance and connects to RabbitMQ.
    """
    def __init__(self):
        self.setup_broker()

    """
    Starts consuming messages from the declared RabbitMQ queue using the given callback.
    Args -> callback (Callable): Function to handle incoming messages. Should accept (channel, method, properties, body).
    """
    def start_broker(self, callback):
        print("Start consuming messages from queue", os.getenv('RABBITMQ_QUEUE'))
        self.channel.basic_consume(queue=os.getenv('RABBITMQ_QUEUE'), on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    """
    Establishes a connection to RabbitMQ and declares the queue.
    Retries connection attempts up to a maximum before failing.
    """
    def setup_broker(self):
        max_retries = 10
        for i in range(max_retries):
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                    host=os.getenv("RABBITMQ_HOST"),
                    port=int(os.getenv("RABBITMQ_PORT")),
                    credentials=pika.PlainCredentials(
                        os.getenv("RABBITMQ_USER"),
                        os.getenv("RABBITMQ_PASSWORD")
                    ),
                    heartbeat=3600,
                ))
                self.channel = self.connection.channel()
                self.channel.queue_declare(queue=os.getenv('RABBITMQ_QUEUE'))
                print("Successful connection to RabbitMQ")
                return
            except Exception as e:
                print(f"RabbitMQ is not ready (attempt {i+1}/{max_retries})")
                time.sleep(2)
        else:
            raise Exception("Could not connect to RabbitMQ after multiple attempts.")

# Instantiate broker when the module is loaded
message_broker = MessageBroker()
