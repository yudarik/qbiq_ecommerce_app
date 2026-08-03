import json
from functools import wraps

from app.cache import redis_client


def cache_ttl(ttl_seconds: int, key_prefix: str):
    """Cache a function's JSON-serializable dict/list return value in Redis for ttl_seconds.

    Cache key is derived from key_prefix plus the function's sorted kwargs, so
    distinct argument combinations get distinct entries.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            client = redis_client.get_redis()
            cache_key = f"{key_prefix}:{json.dumps(kwargs, sort_keys=True)}"

            cached = client.get(cache_key)
            if cached is not None:
                return json.loads(cached)

            result = func(*args, **kwargs)
            client.setex(cache_key, ttl_seconds, json.dumps(result))
            return result

        return wrapper

    return decorator
