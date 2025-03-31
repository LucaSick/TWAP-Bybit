import pika
import os
import time

def close_broker(connection):
    connection.close()

def start_broker(channel, callback):
    print("Start consuming messages from queue", os.getenv('RABBITMQ_QUEUE'))
    channel.basic_consume(queue=os.getenv('RABBITMQ_QUEUE'), on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

def setup_broker():
    max_retries = 10
    for i in range(max_retries):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=os.getenv("RABBITMQ_HOST"),
                port=int(os.getenv("RABBITMQ_PORT")),
                credentials=pika.PlainCredentials(
                    os.getenv("RABBITMQ_USER"),
                    os.getenv("RABBITMQ_PASSWORD")
                ),
                heartbeat=3600,
            ))
            channel = connection.channel()
            channel.queue_declare(queue=os.getenv('RABBITMQ_QUEUE'))
            print("Successful connection to RabbitMQ")
            return connection, channel
        except Exception as e:
            print(f"RabbitMQ is not ready (attempt {i+1}/{max_retries})")
            time.sleep(2)
    else:
        raise Exception("Could not connect to RabbitMQ after multiple attempts.")

queue_connection, queue_channel = setup_broker()