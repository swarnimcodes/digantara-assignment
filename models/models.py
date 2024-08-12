from sqlalchemy import Column, String, DateTime
from pydantic import BaseModel
from datetime import datetime
from utils.database_utils import Base

import pytz

indian_standard_time = pytz.timezone("Asia/Kolkata")


# Job Model
class Job(Base):
    __tablename__ = "jobs"
    id: Column[str] = Column(String, primary_key=True, index=True)
    cron_string = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now(indian_standard_time))
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
