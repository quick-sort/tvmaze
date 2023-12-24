from typing import Dict
from app.api.schema import UserCreate
import app.db.models as models
import app.api.session as http_session
import json
from uuid import UUID, uuid4
import random
import pytest

@pytest.mark.asyncio
async def test_session_backend():
    session_data = http_session.SessionData(user_id=random.randint(1000, 100000))
    session_id = uuid4()
    await http_session.session_storage.create(session_id, session_data)
    data = await http_session.session_storage.read(session_id)
    assert data.user_id == session_data.user_id