import os


class Settings:
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    cache_ttl_seconds: int = int(os.getenv("CACHE_TTL_SECONDS", "60"))
    cors_origins: list[str] = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")


settings = Settings()
