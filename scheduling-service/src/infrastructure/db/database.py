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
                cur = self.connection.cursor()
                cur.execute(f"""
                CREATE TABLE IF NOT EXISTS apscheduler_jobs (
                    id VARCHAR(191) NOT NULL,
                    next_run_time FLOAT(25),
                    job_state BYTEA NOT NULL,
                    PRIMARY KEY (id)
                );
                """)
                cur.execute(f"""
                CREATE TABLE IF NOT EXISTS orders (
                    job_id VARCHAR(60) PRIMARY KEY,
                    symbol VARCHAR(20) NOT NULL,
                    side VARCHAR(10) NOT NULL,
                    size INTEGER NOT NULL,
                    price_limit NUMERIC(18, 8),
                    status VARCHAR(20) CHECK (status IN ('scheduled', 'canceled')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """)
                self.connection.commit()
                return
            except psycopg2.OperationalError as e:
                print(f"Database not ready (attempt {i+1}/{max_retries})")
                time.sleep(2)
        else:
            raise Exception("Could not connect to the database after multiple attempts")

    def close_db_connection(self):
        self.connection.close()

    def add_job_to_db(self, params):
        cur = self.connection.cursor()
        cur.execute("""
            INSERT INTO orders (job_id, symbol, side, size, price_limit, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            params["job_id"],
            params["symbol"],
            params["side"],
            params["size"],
            params["price_limit"],
            params["status"]
        ))
        self.connection.commit()

    def is_canceled(self, job_id):
        cur = self.connection.cursor()
        cur.execute("""
            SELECT status
            FROM orders
            WHERE job_id = %s
        """, (job_id,))
        result = cur.fetchone()
        to_return = (result[0] == 'canceled') if result else False
        return to_return

database = Database()
