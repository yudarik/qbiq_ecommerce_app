from app.cache.decorators import cache_ttl


def test_cache_miss_calls_function():
    call_count = 0

    @cache_ttl(60, key_prefix="test:fn")
    def compute(value: str = "x") -> dict:
        nonlocal call_count
        call_count += 1
        return {"result": value}

    result = compute(value="hello")
    assert result == {"result": "hello"}
    assert call_count == 1


def test_cache_hit_does_not_call_function_again():
    call_count = 0

    @cache_ttl(60, key_prefix="test:hit")
    def compute(value: str = "x") -> dict:
        nonlocal call_count
        call_count += 1
        return {"result": value}

    compute(value="world")
    compute(value="world")
    assert call_count == 1


def test_different_kwargs_produce_distinct_cache_keys():
    call_count = 0

    @cache_ttl(60, key_prefix="test:distinct")
    def compute(value: str = "x") -> dict:
        nonlocal call_count
        call_count += 1
        return {"result": value}

    r1 = compute(value="a")
    r2 = compute(value="b")
    assert r1 == {"result": "a"}
    assert r2 == {"result": "b"}
    assert call_count == 2


def test_cache_returns_list():
    @cache_ttl(60, key_prefix="test:list")
    def get_items(n: int = 3) -> list:
        return [i for i in range(n)]

    result = get_items(n=3)
    assert result == [0, 1, 2]
    cached = get_items(n=3)
    assert cached == [0, 1, 2]
