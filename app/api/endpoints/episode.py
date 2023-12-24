from typing import Any, List, Annotated, Optional, Dict

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, func, distinct, desc
from pydantic import PositiveInt
import logging
logger = logging.getLogger(__name__)
import app.db.models as models
from .. import schema, deps, session as http_session

router = APIRouter()

@router.get("/")
async def search_episodes(
    db: Annotated[Session, Depends(deps.get_db)],
    session_data: Annotated[http_session.SessionData, Depends(deps.get_session)],
    limit: PositiveInt = 10,
    offset: PositiveInt = 0,
    search_field: Optional[str] = None,
    search_value: Optional[str | int | float] = None,
    order: Optional[str] = 'asc',
    orderby: Optional[str] = 'id',
) -> List[schema.TVEpisode]:
    if search_field and search_value:
        if search_field in ['id', 'season', 'number', 'runtime']:
            search_value = int(search_value)
        elif search_field == 'rating_average':
            search_value = float(search_value)
        schema.TVEpisode(**{search_field: search_value})
        stmt = select(models.TVEpisode).where(getattr(models.TVEpisode, search_field) == search_value).limit(limit).offset(offset)
    else:
        stmt = select(models.TVEpisode).limit(limit).offset(offset) 
    if orderby not in schema.TVEpisode.__fields__.keys():
        raise HTTPException(status_code=400, detail="Invalid orderby")
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order")
    if order == 'asc':
        stmt = stmt.order_by(getattr(models.TVEpisode, orderby))
    else:
        stmt = stmt.order_by(desc(getattr(models.TVEpisode, orderby)))
    return db.scalars(stmt).all()

@router.get('/likes')
async def get_liked_episodes(
    db: Annotated[Session, Depends(deps.get_db)],
    session_data: Annotated[http_session.SessionData, Depends(deps.get_session)],
) -> List[schema.TVEpisode]:
    stmt = select(models.UserEpisode).where(and_(models.UserEpisode.user_id == session_data.user_id, models.UserEpisode.like == True))
    links = db.scalars(stmt).all()
    ids = [i.episode_id for i in links]
    stmt = select(models.TVEpisode).where(models.TVEpisode.id.in_(ids))
    return db.scalars(stmt).all()

@router.get('/bookmarks')
async def get_liked_episodes(
    db: Annotated[Session, Depends(deps.get_db)],
    session_data: Annotated[http_session.SessionData, Depends(deps.get_session)],
    person: Optional[str] = None,
    charactor: Optional[str] = None,
) -> List[schema.TVEpisode]:
    stmt = select(models.UserEpisode).where(and_(models.UserEpisode.user_id == session_data.user_id, models.UserEpisode.bookmark == True))
    links = db.scalars(stmt).all()
    ids = [i.episode_id for i in links]
    if person:
        stmt = select(models.TVEpisodeGuestcast.episode_id).select_from(models.TVPeople).join(models.TVPeople.guestcast).where(models.TVPeople.name == person)
        filter_ids = db.scalars(stmt).all()
        ids = list(set(ids) & set(filter_ids))

    if charactor:
        stmt = select(models.TVEpisodeGuestcast.episode_id).select_from(models.TVCharacter).join(models.TVPeople.guestcast).where(models.TVCharacter.name == charactor)
        filter_ids = db.scalars(stmt).all()
        ids = list(set(ids) & set(filter_ids))
    stmt = select(models.TVEpisode).where(models.TVEpisode.id.in_(ids))
    return db.scalars(stmt).all()

@router.get("/{episode_id}")
async def get_episodes(
    db: Annotated[Session, Depends(deps.get_db)],
    session_data: Annotated[http_session.SessionData, Depends(deps.get_session)],
    episode_id: int,
) -> schema.TVEpisode:
    return db.get(models.TVEpisode, episode_id)

@router.get("/{episode_id}/guestcast")
async def get_guestcast(
    db: Annotated[Session, Depends(deps.get_db)],
    session_data: Annotated[http_session.SessionData, Depends(deps.get_session)],
    episode_id: int,
) -> List[Dict[str, str]]:
    user = db.get(models.User, session_data.user_id)
    if not user:
        raise HTTPException(status_code=400, detail="Unauthorized")
    stmt = select(models.TVEpisodeGuestcast).join(models.TVEpisodeGuestcast.character).join(models.TVEpisodeGuestcast.person).where(models.TVEpisodeGuestcast.episode_id == episode_id)
    guestcast = db.scalars(stmt).all()
    for i in guestcast:
        db.refresh(i.person)
        db.refresh(i.character)
    return [{'person': i.person.name, 'character': i.character.name} for i in guestcast]

@router.post("/{episode_id}/do")
async def like_episode(
    db: Annotated[Session, Depends(deps.get_db)],
    session_data: Annotated[http_session.SessionData, Depends(deps.get_session)],
    episode_id: int,
    action: schema.EnumAction, 
) -> schema.Message:
    episode = db.get(models.TVEpisode, episode_id)
    if not episode:
        raise HTTPException(status_code=400, detail="Episode not found")
    user = db.get(models.User, session_data.user_id)
    if not user:
        raise HTTPException(status_code=400, detail="Unauthorized")
    
    stmt = select(models.UserEpisode).where(and_(models.UserEpisode.user_id == user.id, models.UserEpisode.episode_id == episode.id))
    user_episode = db.scalars(stmt).first()
    data = {}
    if action == schema.EnumAction.like:
        data['like'] = True
    elif action == schema.EnumAction.bookmark:
        data['bookmark'] = True
    elif action == schema.EnumAction.unlike:
        data['like'] = False
    elif action == schema.EnumAction.unbookmark:
        data['bookmark'] = False
    if not user_episode:
        user_episode = models.UserEpisode(**data, user_id=user.id, episode_id=episode.id)
    else:
        for k, v in data.items():
            setattr(user_episode, k, v)
    db.add(user_episode)
    db.commit()
    db.refresh(user_episode)

    stmt = select(func.count(distinct(models.UserEpisode.user_id))).select_from(models.UserEpisode).where(and_(models.UserEpisode.episode_id == episode.id, models.UserEpisode.like == True))
    likes = db.scalar(stmt)
    episode.likes = likes
    db.add(episode)
    db.commit()
    db.refresh(episode)
    return schema.Message(message="Success")