import redis

from app.config import settings

_client: redis.Redis | None = None


def get_redis() -> redis.Redis:
    global _client
    if _client is None:
        _client = redis.from_url(settings.redis_url, decode_responses=True)
    return _client


def set_redis(client: redis.Redis) -> None:
    """Override the singleton client. Used by tests to inject fakeredis."""
    global _client
    _client = client
