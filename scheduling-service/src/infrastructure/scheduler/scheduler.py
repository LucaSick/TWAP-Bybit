import os
import uuid
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

"""
Manages job scheduling using APScheduler with a PostgreSQL-backed job store.
"""
class Scheduler:
    """
    Initializes the Scheduler instance and configures the job store.
    """
    def __init__(self):
        self.create_scheduler()

    """
    Sets up the BackgroundScheduler with a SQLAlchemy job store connected to PostgreSQL.
    """
    def create_scheduler(self):
        jobstores = {
            'default': SQLAlchemyJobStore(
                url=f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DATABASE')}"
            )
        }

        self.scheduler = BackgroundScheduler(jobstores=jobstores)

    """
    Starts the scheduler in the background.
    """
    def setup_scheduler(self):
        print("Starting scheduler")
        self.scheduler.start()

    """
    Shuts down the scheduler and terminates any background job execution.
    """
    def shutdown_scheduler(self):
        self.scheduler.shutdown()

    """
    Schedules a recurring job with an interval delay until a specified end datetime.
    Args ->
        send_order (Callable): The function to execute.
        delay (int): The interval between executions in seconds.
        end_datetime (datetime): The time at which job execution should stop.
        params (dict): Parameters passed as kwargs to the job function.
    Returns -> dict: The updated parameters including a generated job_id and status.
    """
    def add_job(self, send_order, delay, end_datetime, params):
        print(f"Creating jobs with following params: {params}")
        timestamp = int(time.time() * 1000)
        generated_id = str(uuid.uuid4())
        job_id = f"{generated_id}-{timestamp}"
        params["job_id"] = job_id
        self.scheduler.add_job(send_order, 'interval', id=job_id, seconds=delay, end_date=end_datetime, kwargs=params)
        params["status"] = "scheduled"
        return params

    """
    Removes a scheduled job using its ID.
    Args -> job_id (str): The ID of the job to remove.
    """
    def remove_job(self, job_id):
        self.scheduler.remove_job(job_id)

scheduler = Scheduler()
