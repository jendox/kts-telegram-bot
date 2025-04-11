import os
import typing

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from data_service.store.database.sqlalchemy_base import BaseModel

__all__ = ("Database",)

if typing.TYPE_CHECKING:
    from data_service.web.app import Application


class Database:
    def __init__(self, app: "Application"):
        self.app = app
        self.engine: AsyncEngine | None = None
        self._db: type[DeclarativeBase] = BaseModel
        self.session: async_sessionmaker[AsyncSession] | None = None

    async def connect(self, *args, **kwargs) -> None:
        self.engine = create_async_engine(
            URL.create(
                drivername=os.getenv("POSTGRES_DRIVER_NAME"),
                username=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                host=os.getenv("POSTGRES_HOST"),
                port=os.getenv("POSTGRES_PORT"),
                database=os.getenv("POSTGRES_DB"),
            ),
            echo=True,
        )
        self.session = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession,
            autoflush=False,
            autocommit=False,
        )

    async def disconnect(self, *args, **kwargs) -> None:
        if self.engine:
            await self.engine.dispose()
