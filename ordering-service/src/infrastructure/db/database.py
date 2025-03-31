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
            print("Successfull connection to PostgreSQL")
            return conn
        except psycopg2.OperationalError as e:
            print(f"Database not ready (attempt {i+1}/{max_retries})")
            time.sleep(2)
    else:
        raise Exception("Could not connect to the database after multiple attempts")

def close_db_connection(connection):
    connection.close()

def cancel_job(connection, job_id):
    print("Cancelling job for", job_id)
    cur = connection.cursor()
    cur.execute("""
        UPDATE orders
        SET status = 'canceled'
        WHERE job_id = %s
    """, (job_id,))
    connection.commit()

db_connection = setup_database()
