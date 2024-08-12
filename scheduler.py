# Main
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel
from datetime import datetime, timezone
import uuid
import croniter
import threading
from typing import List
import time
import pytz

ist = pytz.timezone("Asia/Kolkata")

# Custom Middlewares
from middlewares.log_headers import log_headers

# Routers
from routes.hello import router as hello_router


app = FastAPI()

# CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Registering Custom Middlewares
app.middleware("http")(log_headers)

# Routes
app.include_router(hello_router)


# Database Setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./database/job_scheduler.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Job Model
class Job(Base):
    __tablename__ = "jobs"
    id: str = Column(String, primary_key=True, index=True)
    cron_string = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now(ist))
    last_run = Column(DateTime, nullable=True)
    next_run = Column(DateTime)


Base.metadata.create_all(bind=engine)


# Pydantic Models
class JobCreate(BaseModel):
    cron_string: str


class JobResponse(BaseModel):
    id: str
    cron_string: str
    created_at: datetime
    last_run: datetime | None
    next_run: datetime


# DB
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Helper func to generate time based unique IDs
def generate_id():
    return str(uuid.uuid1())


# Helper func to calculate next run time
def calculate_next_run(cron_string: str):
    cron = croniter.croniter(cron_string, datetime.now(ist))
    return cron.get_next(datetime)


# Create new jobs and add it to database queue
@app.post("/jobs", response_model=JobResponse)
def create_jobs(job: JobCreate, db: Session = Depends(get_db)):
    next_run = calculate_next_run(job.cron_string)
    db_job = Job(id=generate_id(), cron_string=job.cron_string, next_run=next_run)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


# Get all scheduled jobs
@app.get("/jobs", response_model=List[JobResponse])
def list_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = db.query(Job).offset(skip).limit(limit).all()
    return jobs


# Get job details by id
@app.get("/jobs/{job_id}", response_model=JobResponse)
def get_job_by_id(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


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


threading.Thread(target=run_jobs, daemon=True).start()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
