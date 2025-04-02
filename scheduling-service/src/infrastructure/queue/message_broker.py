import pika
import os
import time
import json

class MessageBroker:
    def __init__(self):
        self.setup_broker()

    def send_message(self, body):
        print(f"Making an order: {body}")
        message = json.dumps(body).encode('utf-8')
        self.channel.basic_publish(exchange='', routing_key=os.getenv('RABBITMQ_QUEUE'), body=message)

    def close_broker(self):
        self.connection.close()

    def setup_broker(self):
        max_retries = 10
        for i in range(max_retries):
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                    heartbeat=3600,
                    host=os.getenv("RABBITMQ_HOST"),
                    port=int(os.getenv("RABBITMQ_PORT")),
                    credentials=pika.PlainCredentials(
                        os.getenv("RABBITMQ_USER"),
                        os.getenv("RABBITMQ_PASSWORD")
                    )
                ))
                self.channel = self.connection.channel()
                self.channel.queue_declare(queue=os.getenv('RABBITMQ_QUEUE'))
                return
            except Exception as e:
                print(f"RabbitMQ is not ready (attempt {i+1}/{max_retries})")
                time.sleep(2)
        else:
            raise Exception("Could not connect to RabbitMQ after multiple attempts.")

message_broker = MessageBroker()
