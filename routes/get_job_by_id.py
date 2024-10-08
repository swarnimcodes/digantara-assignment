from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from models.models import JobResponse, Job

from utils.database_utils import get_db


router = APIRouter()


# Get job details by id
@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_job_by_id(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
