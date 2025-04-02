import psycopg2
import os
import time

class Database:
    def __init__(self):
        self.setup_database()

    def setup_database(self):
        max_retries = 10
        for i in range(max_retries):
            try:
                self.connection = psycopg2.connect(database=os.getenv('POSTGRES_DATABASE'),
                                            user=os.getenv('POSTGRES_USER'),
                                            host=os.getenv('POSTGRES_HOST'),
                                            password=os.getenv('POSTGRES_PASSWORD'),
                                            port=os.getenv('POSTGRES_PORT'))
                print("Successfull connection to PostgreSQL")
                return
            except psycopg2.OperationalError as e:
                print(f"Database not ready (attempt {i+1}/{max_retries})")
                time.sleep(2)
        else:
            raise Exception("Could not connect to the database after multiple attempts")

    def cancel_job(self, job_id):
        print("Cancelling job for", job_id)
        cur = self.connection.cursor()
        cur.execute("""
            UPDATE orders
            SET status = 'canceled'
            WHERE job_id = %s
        """, (job_id,))
        self.connection.commit()

database = Database()
