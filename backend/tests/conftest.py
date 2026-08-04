import fakeredis
import pytest
from fastapi.testclient import TestClient

import app.cache.redis_client as redis_client_module
from app.main import app


@pytest.fixture(autouse=True)
def fake_redis():
    """Replace the Redis singleton with an in-memory fakeredis for all tests."""
    client = fakeredis.FakeStrictRedis(decode_responses=True)
    redis_client_module.set_redis(client)
    yield client
    redis_client_module.set_redis(None)


@pytest.fixture
def api_client():
    return TestClient(app)
