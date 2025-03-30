import psycopg2
import os
import time

def setup_database():
    max_retries = 10
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(database=os.getenv('POSTGRES_DATABASE'),
                                        user=os.getenv('POSTGRES_USER'),
                                        host=os.getenv('POSTGRES_HOST'),
                                        password=os.getenv('POSTGRES_PASSWORD'),
                                        port=os.getenv('POSTGRES_PORT'))
            cur = conn.cursor()
            cur.execute(f"""
            CREATE TABLE IF NOT EXISTS apscheduler_jobs (
                id VARCHAR(191) NOT NULL,
                next_run_time FLOAT(25),
                job_state BYTEA NOT NULL,
                PRIMARY KEY (id)
            );
            """)
            conn.commit()
            return conn, cur
        except psycopg2.OperationalError as e:
            print(f"Database not ready (attempt {i+1}/{max_retries})")
            time.sleep(2)
    else:
        raise Exception("Could not connect to the database after multiple attempts")