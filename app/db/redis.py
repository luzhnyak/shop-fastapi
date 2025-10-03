from typing import Optional
import redis

from app.core.config import settings


class RedisService:
    _instance: Optional["RedisService"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_client()
        return cls._instance

    def _init_client(self):
        self.redis_url = settings.redis.REDIS_URL
        self.redis_client = redis.asyncio.from_url(
            self.redis_url,
            decode_responses=True,
        )

    async def get(self, key):
        return await self.redis_client.get(key)

    async def set(self, key, value):
        return await self.redis_client.set(key, value)

    async def setex(self, key: str, ttl: int, value: str):
        return await self.redis_client.setex(key, ttl, value)

    async def keys(self, pattern: str):
        return await self.redis_client.keys(pattern)

    async def delete(self, key: str):
        return await self.redis_client.delete(key)
