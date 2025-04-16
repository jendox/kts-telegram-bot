import enum
import os

__all__ = (
    "StorageType",
    "get_storage",
)

from shared.storage.base import Storage
from shared.storage.redis import RedisStorage


class StorageType(enum.Enum):
    Redis = "redis"


def get_storage(storage_type: StorageType) -> Storage:
    if storage_type == StorageType.Redis:
        return RedisStorage(os.getenv("REDIS_URL"))

    raise ValueError(f"Unsupported storage type: {storage_type.value}")
