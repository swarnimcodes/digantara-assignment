from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from functools import lru_cache

from sqlalchemy.orm import Session
from models.models import JobResponse, JobCreate, Job

from utils.utils import calculate_next_run, generate_id
from utils.database_utils import get_db

router = APIRouter()


# Create new jobs and add it to database queue
@router.post("/jobs", response_model=JobResponse)
def create_jobs(job: JobCreate, db: Session = Depends(get_db)):
    next_run = calculate_next_run(job.cron_string)
    db_job = Job(id=generate_id(), cron_string=job.cron_string, next_run=next_run)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job
