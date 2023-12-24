from typing import Dict, Generator
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.db import models
from app.db.session import SessionLocal
import pytest
import os
import datetime

@pytest.fixture(scope='session')
def api_key_header() -> Dict[str, str]:
    return {
        'api-key': os.environ.get('API_KEY'),
    }

@pytest.fixture(scope='session')
def job_obj_in() -> Dict[str, str]:
    return {
        "date": datetime.date.today().strftime('%Y-%m-%d'),
        "country": 'US'
    }

@pytest.fixture(scope="session")
def user_obj_in() -> Dict[str, str]:
    return {
        'full_name': 'test_user',
        'email': 'test_api@test.com',
        'password': 'plain_password',
    }

@pytest.fixture(scope="session")
def db() -> Generator:
    session = SessionLocal()
    models.Base.metadata.create_all(bind=session.get_bind(), checkfirst=True)
    yield session


@pytest.fixture(scope="session")
def client(
    db: Session,
) -> Generator:
    with TestClient(app) as c:
        yield c