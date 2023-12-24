from typing import Optional
import datetime
from pydantic import BaseModel
from app.db.models.job import JobStatus

class JobBase(BaseModel):
    date: datetime.date
    country: str = 'US'

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int
    status: JobStatus
    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None
    msg: Optional[str] = None