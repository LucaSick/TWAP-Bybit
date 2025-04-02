import os
import uuid
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

class Scheduler:
    def __init__(self):
        self.create_scheduler()

    def create_scheduler(self):
        jobstores = {
            'default': SQLAlchemyJobStore(
                url=f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DATABASE')}"
            )
        }

        self.scheduler = BackgroundScheduler(jobstores=jobstores)

    def setup_scheduler(self):
        print("Starting scheduler")
        self.scheduler.start()

    def shutdown_scheduler(self):
        self.scheduler.shutdown()

    def add_job(self, send_order, delay, end_datetime, params):
        print(f"Creating jobs with following params: {params}")
        timestamp = int(time.time() * 1000)
        generated_id = str(uuid.uuid4())
        job_id = f"{generated_id}-{timestamp}"
        params["job_id"] = job_id
        self.scheduler.add_job(send_order, 'interval', id=job_id, seconds=delay, end_date=end_datetime, kwargs=params)
        params["status"] = "scheduled"
        return params
    
    def remove_job(self, job_id):
        self.scheduler.remove_job(job_id)

scheduler = Scheduler()
