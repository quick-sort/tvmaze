from typing import Generator, Annotated

from fastapi import Depends, HTTPException, Header, Response
from app.config import settings
from app.db import models
from uuid import UUID
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from . import session as http_session

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_api_key(
    api_key: Annotated[str | None, Header()],
) -> str:
    if api_key and api_key == settings.API_KEY:
        return api_key
    raise HTTPException(
        status_code=400,
        detail="Unauthorized",
    )

async def get_session(
    session_id: Annotated[UUID, Depends(http_session.cookie)],
    session_data: Annotated[http_session.SessionData, Depends(http_session.session)],
    response: Response
) -> Generator:
    if not session_data:
        if isinstance(session_id, UUID):
            await http_session.session_storage.delete(session_id)
        http_session.cookie.delete_from_response(response)
        raise HTTPException(status_code=400, detail="Unauthorized")
    return session_data