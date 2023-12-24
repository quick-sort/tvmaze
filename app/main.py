from typing import List
from fastapi import FastAPI
from sqlalchemy import select, func, delete
from app.config import settings
from app.api.endpoints import api_router
import logging
import httpx
import asyncio
import datetime

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_STR)

@app.on_event("startup")
async def init_db():
    import app.db.models as models
    from app.db.session import engine, SessionLocal
    models.Base.metadata.create_all(bind=engine, checkfirst=True)
    if settings.TESTING:
        return
    with SessionLocal() as db:
        episode_count = db.scalar(
            select(func.count(models.TVEpisode.id)).select_from(models.TVEpisode)
        )
        if episode_count == 0:
            db.execute(delete(models.Job))
            import app.db.models as models
            d = datetime.date.today()
            ids = []
            dates = [d - datetime.timedelta(days=i) for i in range(1, 8)]
            for i in dates:
                job = models.Job(date=i, country=settings.DEFAULT_JOB_COUNTRY)
                db.add(job)
                db.commit()
                db.refresh(job)
                ids.append(job.id)
            asyncio.create_task(trigger_jobs(ids))

async def trigger_job(i):
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f'http://127.0.0.1{settings.API_STR}/jobs/{i}/restart',
            headers={'api-key': settings.API_KEY}
        )
        if r.status_code != 200:
            await asyncio.sleep(60)
            r = await trigger_job(i)
        return r
    
async def await_job(i):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f'http://127.0.0.1{settings.API_STR}/jobs/{i}',
            headers={'api-key': settings.API_KEY}
        )
        if r.status_code != 200:
            await asyncio.sleep(60)
            r = await await_job(i)
        r = r.json()
        if r['status'] == 'running':
            await asyncio.sleep(60)
            r = await await_job(i)
        elif r['status'] == 'failed':
            await trigger_job(i)
            r = await_job(i)
        return r

async def trigger_jobs(ids):
    for i in ids:
        r = await trigger_job(i)
        r = await await_job(i)
