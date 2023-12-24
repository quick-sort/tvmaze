from typing import Dict, Any
from fastapi.testclient import TestClient
from app.api.schema import UserCreate
from app.config import settings
import json
import logging
logger = logging.getLogger(__name__)

def test_user(
    client: TestClient,
    user_obj_in: Dict[str, str],    
) -> None:
    r = client.get(
        f"{settings.API_STR}/users/self",
    )
    assert r.status_code == 400

    data = dict(user_obj_in)
    r = client.post(
        f"{settings.API_STR}/users/registry",
        json=data
    )
    assert r.status_code == 200
    assert r.json()['id'] is not None
    user_id = r.json()['id']

    r = client.get(
        f"{settings.API_STR}/users/self",
        cookies=r.cookies,
    )
    assert r.status_code == 200
    assert r.json()['id'] == user_id

    r = client.get(
        f"{settings.API_STR}/users/logout",
        cookies=r.cookies,
    )
    assert r.status_code == 200

    
    r = client.get(
        f"{settings.API_STR}/users/self",
        cookies=r.cookies,
    )
    assert r.status_code == 400

    r = client.post(
        f"{settings.API_STR}/users/login",
        cookies=r.cookies,
        json=data
    )
    assert r.status_code == 200
    assert r.json()['id'] == user_id

    r = client.get(
        f"{settings.API_STR}/users/self",
        cookies=r.cookies,
    )
    assert r.status_code == 200
    assert r.json()['id'] == user_id