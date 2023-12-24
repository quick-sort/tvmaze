from typing import Optional
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String, ForeignKey, DateTime
import datetime
from .base import Base
import enum

class JobStatus(enum.Enum):
    pending = 'pending'
    running = 'running'
    done = 'done'
    failed = 'failed'

class Job(Base):
    __tablename__ = "job"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column(index=True)
    country: Mapped[str] = mapped_column(String(128), index=True)
    status: Mapped[JobStatus] = mapped_column(default=JobStatus.pending)
    start_time: Mapped[Optional[datetime.datetime]]
    end_time: Mapped[Optional[datetime.datetime]]
    msg: Mapped[Optional[str]] = mapped_column(String(1024))