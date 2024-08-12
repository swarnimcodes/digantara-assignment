import uuid
import croniter
from datetime import datetime
import pytz
import time


from utils.database_utils import SessionLocal
from models.models import Job

ist = pytz.timezone("Asia/Kolkata")


# Helper func to generate time based unique IDs
def generate_id():
    return str(uuid.uuid1())


# Helper func to calculate next run time
def calculate_next_run(cron_string: str):
    cron = croniter.croniter(cron_string, datetime.now(ist))
    return cron.get_next(datetime)


# Dummy task
def number_crunching_task():
    print("running task")
    result = 0
    for i in range(1000000):
        result += i
    return result


# Run tasks in background
def run_jobs():
    while True:
        with SessionLocal() as db:
            current_time = datetime.now(ist)
            jobs_to_run = db.query(Job).filter(Job.next_run <= current_time).all()

            for job in jobs_to_run:
                number_crunching_task()

                job.last_run = current_time
                job.next_run = calculate_next_run(job.cron_string)
                db.commit()
        time.sleep(1)
