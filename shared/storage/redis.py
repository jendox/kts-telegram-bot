from functools import wraps
from logging import getLogger

import redis
from redis.asyncio import ConnectionPool, Redis

from shared.storage.base import Storage

__all__ = ("RedisStorage",)


def check_client_connection(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if self._client is None:
            raise ConnectionError("Redis client is not connected")
        return await func(self, *args, **kwargs)

    return wrapper


class RedisStorage(Storage):
    def __init__(self, url: str):
        super().__init__(url)
        self.logger = getLogger(self.__class__.__name__)
        self._pool: ConnectionPool | None = None
        self._client: Redis | None = None

    async def start(self) -> None:
        try:
            self._pool = ConnectionPool.from_url(self.url)
            self._client = await Redis(connection_pool=self._pool)
            self.logger.info("Redis connection successfully established")
        except redis.exceptions.ConnectionError as e:
            self.logger.error("Redis client is not connected: %s", str(e))
            raise
        except redis.exceptions.RedisError as e:
            self.logger.error("General Redis error: %s", str(e))
            raise

    async def stop(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self.logger.info("Redis connection closed")
        else:
            self.logger.info("Redis connection is already none")

    async def set(self, name: str, key: str, value: str) -> None:
        try:
            await self._client.hset(name, key, value)
        except redis.exceptions.RedisError as e:
            self.logger.error("Error setting value in Redis: %s", str(e))
            raise

    async def get(self, name: str, key: str) -> str | None:
        try:
            value = await self._client.hget(name, key)
            return value.decode() if value is not None else value
        except redis.exceptions.RedisError as e:
            self.logger.error("Error getting value from Redis: %s", str(e))
            raise

    async def clear(self, name: str) -> None:
        try:
            await self._client.unlink(name)
        except redis.exceptions.RedisError as e:
            self.logger.error("Error setting value in Redis: %s", str(e))
            raise
