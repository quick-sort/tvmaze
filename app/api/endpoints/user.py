from typing import Any, List, Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from uuid import UUID, uuid4
import app.db.models as models
from app.utils import get_password_hash, verify_password
from .. import schema, deps, session as http_session
router = APIRouter()

@router.get("/")
async def list_users(
    db: Annotated[Session, Depends(deps.get_db)],
    api_key: Annotated[str, Depends(deps.get_api_key)],
) -> List[schema.User]:
    return db.scalars(select(models.User)).all()

@router.post("/registry")
async def registry(
    db: Annotated[Session, Depends(deps.get_db)],
    user_obj_in: schema.UserCreate,
    response: Response
) -> schema.User:
    user = models.User(
        email=user_obj_in.email,
        hashed_password=get_password_hash(user_obj_in.password),
        full_name=user_obj_in.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    session_id = uuid4()
    session_data = http_session.SessionData(user_id=user.id)
    await http_session.session_storage.create(session_id, session_data)
    http_session.cookie.attach_to_response(response, session_id)
    return user

@router.get("/self")
async def get_current_user(
    db: Annotated[Session, Depends(deps.get_db)],
    session_id: Annotated[UUID, Depends(http_session.cookie)],
    session_data: Annotated[http_session.SessionData, Depends(deps.get_session)],
    response: Response
) -> schema.User:
    user = db.get(models.User, session_data.user_id)
    if not user:
        http_session.cookie.delete_from_response(response)
        await http_session.session_storage.delete(session_id)
        raise HTTPException(status_code=400, detail="User not found")
    return user

@router.post("/login")
async def login(
    db: Annotated[Session, Depends(deps.get_db)],
    user_obj_in: schema.UserLogin,
    response: Response
) -> schema.User: 
    user = db.scalar(select(models.User).where(models.User.email == user_obj_in.email))
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not verify_password(user_obj_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    session_id = uuid4()
    session_data = http_session.SessionData(user_id=user.id)
    await http_session.session_storage.create(session_id, session_data)
    http_session.cookie.attach_to_response(response, session_id)
    return user

@router.get("/logout")
async def logout(
    session_id: Annotated[UUID, Depends(http_session.cookie)],
    response: Response
) -> schema.Message:
    http_session.cookie.delete_from_response(response)
    await http_session.session_storage.delete(session_id)
    return schema.Message(message="logout success")