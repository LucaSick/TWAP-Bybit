import os

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

def create_scheduler():
    jobstores = {
        'default': SQLAlchemyJobStore(
            url=f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DATABASE')}"
        )
    }

    background_scheduler = BackgroundScheduler(jobstores=jobstores)
    return background_scheduler

def setup_sched(scheduler: BackgroundScheduler):
    background_scheduler.start()

def shutdown_scheduler(scheduler: BackgroundScheduler):
    scheduler.shutdown()
    return

def add_job(scheduler: BackgroundScheduler, send_order, delay, end_datetime, params_list):
    print(f"Creating jobs with following params: {params_list}")
    scheduler.add_job(send_order, 'interval', params_list, seconds=delay, end_date=end_datetime)