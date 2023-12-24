from uuid import UUID, uuid4
from typing import Optional
from fastapi_sessions.backends import SessionBackend
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import CookieParameters  # noqa
from fastapi_sessions.frontends.implementations import SessionCookie  # noqa
from fastapi_sessions.session_verifier import SessionVerifier
from pydantic import BaseModel
import redis.asyncio as redis
#import redis
from fastapi import HTTPException
import pickle
from app.config import settings
import json

class SessionData(BaseModel):
    user_id: int

class RedisSessionBackend(SessionBackend[UUID, SessionData]):
    def __init__(self, host: str, port: int):
        self.client = redis.Redis(host=host, port=port)

    async def create(self, session_id: UUID, data: SessionData) -> None:
        await self.update(session_id, data)

    async def read(self, session_id: UUID) -> Optional[SessionData]:
        raw = await self.client.get(session_id.bytes)
        return raw and pickle.loads(raw)
    
    async def update(self, session_id: UUID, data: SessionData) -> None:
        await self.client.set(session_id.bytes, pickle.dumps(data))

    async def delete(self, session_id: UUID) -> None:
        await self.client.delete(session_id.bytes)

class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
        self,
        *,
        identifier: str,
        auto_error: bool,
        backend: RedisSessionBackend,
        auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        return True
    
cookie_params = CookieParameters()

cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=False,
    secret_key="DONOTUSE",
    cookie_params=cookie_params,
)
if not settings.REDIS_HOST:
    session_storage = InMemoryBackend[UUID, SessionData]()
else:
    session_storage = RedisSessionBackend(settings.REDIS_HOST, settings.REDIS_PORT)
session = BasicVerifier(
    identifier="general_verifier",
    auto_error=False,
    backend=session_storage,
    auth_http_exception=HTTPException(status_code=400, detail="invalid session"),
)
 
