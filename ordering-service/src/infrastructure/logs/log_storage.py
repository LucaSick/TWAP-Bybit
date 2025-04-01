from pymongo import MongoClient
import os
import time

class LogStorage:
    def __init__(self):
        self.setup_client()

    def setup_client(self):
        max_retries = 10
        for i in range(max_retries):
            try:
                self.client = MongoClient(f"{os.getenv('MONGODB_HOST')}://{os.getenv('MONGODB_USER')}:{os.getenv('MONGODB_PASSWORD')}@{os.getenv('MONGODB_HOST')}:{os.getenv('MONGODB_PORT')}/")
                self.order_db = self.client["orders"]
                self.collection = self.order_db["order_logs"]
                print("Connection with MongoDB established")
                return
            except Exception as e:
                print(f"MongoDB not ready (attempt {i+1}/{max_retries})")
                time.sleep(5)
        else:
            raise Exception("Could not connect to the database after multiple attempts")
    
    def insert_value(self, body):
        self.collection.insert_one(body)
        print("Log added:", body)

log_storage = LogStorage()

