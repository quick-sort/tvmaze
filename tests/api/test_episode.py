from typing import Dict, Any
from fastapi.testclient import TestClient
import app.api.schema as schema
from app.config import settings
import json
import logging
logger = logging.getLogger(__name__)


def test_episode(
    client: TestClient,
    user_obj_in: Dict[str, str], 
) -> None:
    r = client.post(
        f"{settings.API_STR}/users/login",
        json=user_obj_in
    )
    assert r.status_code == 200

    r = client.get(
        f"{settings.API_STR}/episodes",
        cookies=r.cookies,
    )
    assert r.status_code == 200
    data = r.json()
    assert len(data) > 0

    person = None
    character = None
    episode_id = None
    episode_id2 = data[0]['id']
    for i in data[1:]:
        episode_id = i['id']
        r = client.get(
            f"{settings.API_STR}/episodes/{episode_id}/guestcast",
            cookies=r.cookies,
        )
        assert r.status_code == 200
        d = r.json()
        if d:
            person = d[0]['person']
            character = d[0]['character']
            break
    assert episode_id is not None
    assert episode_id2 is not None
    assert person is not None
    assert character is not None

    r = client.post(
        f"{settings.API_STR}/episodes/{episode_id}/do?action=like",
        cookies=r.cookies,
    )
    assert r.status_code == 200

    r = client.get(
        f"{settings.API_STR}/episodes/{episode_id}",
        cookies=r.cookies,
    )
    assert r.status_code == 200
    data = r.json()
    assert data['likes'] == 1

    r = client.post(
        f"{settings.API_STR}/episodes/{episode_id}/do?action=unlike",
        cookies=r.cookies,
    )
    assert r.status_code == 200

    r = client.get(
        f"{settings.API_STR}/episodes/{episode_id}",
        cookies=r.cookies,
    )
    assert r.status_code == 200
    data = r.json()
    assert data['likes'] == 0

    r = client.post(
        f"{settings.API_STR}/episodes/{episode_id}/do?action=bookmark",
        cookies=r.cookies,
    )
    assert r.status_code == 200

    r = client.post(
        f"{settings.API_STR}/episodes/{episode_id2}/do?action=bookmark",
        cookies=r.cookies,
    )
    assert r.status_code == 200

    r = client.get(
        f"{settings.API_STR}/episodes/bookmarks",
        cookies=r.cookies,
    )
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 2

    r = client.get(
        f"{settings.API_STR}/episodes/bookmarks?person={person}",
        cookies=r.cookies,
    )
    assert r.status_code == 200
    data = r.json()
    assert len(data) > 0 and len(data) <= 2

    r = client.get(
        f"{settings.API_STR}/episodes/bookmarks?character={character}",
        cookies=r.cookies,
    )
    assert r.status_code == 200
    data = r.json()
    assert len(data) > 0 and len(data) <= 2

    r = client.get(
        f"{settings.API_STR}/episodes/bookmarks?person=notexist",
        cookies=r.cookies,
    )
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 0

    r = client.post(
        f"{settings.API_STR}/episodes/{episode_id}/do?action=unbookmark",
        cookies=r.cookies,
    )
    assert r.status_code == 200

    r = client.get(
        f"{settings.API_STR}/episodes/bookmarks",
        cookies=r.cookies,
    )
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1

