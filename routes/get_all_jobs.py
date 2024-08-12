from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from models.models import JobResponse, Job

from utils.database_utils import get_db

from typing import List

router = APIRouter()


# Get all scheduled jobs
@router.get("/jobs", response_model=List[JobResponse])
def list_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = db.query(Job).offset(skip).limit(limit).all()
    return jobs
