from typing import Dict, Any
from fastapi.testclient import TestClient
import app.api.schema as schema
from app.config import settings
import json
import logging
logger = logging.getLogger(__name__)


def test_job(
    client: TestClient,
    job_obj_in: Dict[str, str],
    api_key_header: Dict[str, str],
) -> None:
    headers = {
        'Content-Type': 'application/json',
    }
    headers.update(**api_key_header)
    r = client.post(
        f"{settings.API_STR}/jobs",
        headers=headers,
        json=job_obj_in
    )
    assert r.status_code == 200
    job = r.json()
    assert job['id'] is not None
    assert job['status'] == 'pending'