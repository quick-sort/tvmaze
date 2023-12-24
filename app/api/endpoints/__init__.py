from fastapi import APIRouter

from . import episode, user, job

api_router = APIRouter()
api_router.include_router(episode.router, prefix="/episodes", tags=["episodes"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(job.router, prefix="/jobs", tags=["jobs"])