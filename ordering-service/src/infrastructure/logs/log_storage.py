from pymongo import MongoClient
import os
import time

"""
Handles interaction with MongoDB for storing and logging order-related information.
"""
class LogStorage:
    """
    Initializes the LogStorage instance and connects to MongoDB.
    """
    def __init__(self):
        self.setup_client()

    """
    Connects to MongoDB using environment variables.
    Retries connection several times before raising an exception.
    """
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
                time.sleep(2)
        else:
            raise Exception("Could not connect to the database after multiple attempts")

    """
    Inserts a log entry into the MongoDB `order_logs` collection.
    Args -> body (dict): The log document to be inserted.
    """
    def insert_value(self, body):
        self.collection.insert_one(body)
        print("Log added:", body)

# Initialize the MongoDB logger when the module is loaded
log_storage = LogStorage()
