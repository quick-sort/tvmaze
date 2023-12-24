from typing import Any, List, Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, BackgroundTasks, WebSocket
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, desc
from uuid import UUID, uuid4
import app.db.models as models
from app.job.crawl import crawl
import time
from .. import schema, deps
router = APIRouter()

@router.post("/")
def create_job(
    db: Annotated[Session, Depends(deps.get_db)],
    api_key: Annotated[str, Depends(deps.get_api_key)],
    background_tasks: BackgroundTasks,
    job_obj_in: schema.JobCreate,
) -> schema.Job:
    job_obj = models.Job(date=job_obj_in.date, country=job_obj_in.country)
    db.add(job_obj)
    db.commit()
    db.refresh(job_obj)
    background_tasks.add_task(crawl, job_obj.id)
    return job_obj

@router.get("/")
def list_job(
    db: Annotated[Session, Depends(deps.get_db)],
    api_key: Annotated[str, Depends(deps.get_api_key)],
) -> List[schema.Job]:
    return db.scalars(select(models.Job).order_by(desc(models.Job.date))).all()

@router.get("/{job_id}")
def get_job(
    db: Annotated[Session, Depends(deps.get_db)],
    api_key: Annotated[str, Depends(deps.get_api_key)],
    job_id: int,
) -> schema.Job:
    return db.get(models.Job, job_id)

@router.post("/{job_id}/restart")
def restart_job(
    db: Annotated[Session, Depends(deps.get_db)],
    api_key: Annotated[str, Depends(deps.get_api_key)],
    background_tasks: BackgroundTasks,
    job_id: int,
) -> schema.Job:
    job = db.get(models.Job, job_id)
    background_tasks.add_task(crawl, job.id)
    return job