import pika
import os
import time
import json

def send_message(channel, body):
    print(f"Making an order: {body}")
    message = json.dumps(body).encode('utf-8')
    channel.basic_publish(exchange='', routing_key=os.getenv('RABBITMQ_QUEUE'), body=message)

def close_broker(connection):
    connection.close()

def setup_broker():
    max_retries = 10
    for i in range(max_retries):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                heartbeat=3600,
                host=os.getenv("RABBITMQ_HOST"),
                port=int(os.getenv("RABBITMQ_PORT")),
                credentials=pika.PlainCredentials(
                    os.getenv("RABBITMQ_USER"),
                    os.getenv("RABBITMQ_PASSWORD")
                )
            ))
            channel = connection.channel()
            channel.queue_declare(queue=os.getenv('RABBITMQ_QUEUE'))
            return connection, channel
        except Exception as e:
            print(f"RabbitMQ is not ready (attempt {i+1}/{max_retries})")
            time.sleep(2)
    else:
        raise Exception("Could not connect to RabbitMQ after multiple attempts.")

queue_connection, queue_channel = setup_broker()