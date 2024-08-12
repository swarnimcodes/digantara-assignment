from sqlalchemy import create_engine, Column, String, DateTime
from pydantic import BaseModel
from datetime import datetime
import pytz

ist = pytz.timezone("Asia/Kolkata")


# Job Model
class Job(Base):
    __tablename__ = "jobs"
    id: Column[str] = Column(String, primary_key=True, index=True)
    cron_string = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now(ist))
    last_run = Column(DateTime, nullable=True)
    next_run = Column(DateTime)


# Pydantic Models
class JobCreate(BaseModel):
    cron_string: str


class JobResponse(BaseModel):
    id: str
    cron_string: str
    created_at: datetime
    last_run: datetime | None
    next_run: datetime
