import os
import uuid
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

def create_scheduler():
    jobstores = {
        'default': SQLAlchemyJobStore(
            url=f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DATABASE')}"
        )
    }

    scheduler = BackgroundScheduler(jobstores=jobstores)
    return scheduler

def setup_sched(scheduler: BackgroundScheduler):
    scheduler.start()

def shutdown_scheduler(scheduler: BackgroundScheduler):
    scheduler.shutdown()
    return

def add_job(scheduler: BackgroundScheduler, send_order, delay, end_datetime, params):
    print(f"Creating jobs with following params: {params}")
    timestamp = int(time.time() * 1000)
    generated_id = str(uuid.uuid4())
    job_id = f"{generated_id}-{timestamp}"
    params["job_id"] = job_id
    scheduler.add_job(send_order, 'interval', id=job_id, seconds=delay, end_date=end_datetime, kwargs=params)
    params["status"] = "scheduled"
    return params

background_scheduler = create_scheduler()