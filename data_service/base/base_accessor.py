import typing
from typing import Callable, AsyncIterator
from contextlib import asynccontextmanager
from functools import wraps
from logging import getLogger

if typing.TYPE_CHECKING:
    from data_service.web.app import Application
    from sqlalchemy.ext.asyncio import AsyncSession


def with_session(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        async with self.get_session() as session:
            return await func(self, session, *args, **kwargs)

    return wrapper


class BaseAccessor:
    def __init__(
            self,
            app: "Application",
            session_factory: Callable[[], "AsyncSession"] | None = None,
            *args,
            **kwargs
    ):
        self.app = app
        self.logger = getLogger(f"{self.__class__.__name__}")
        self.session_factory = session_factory

        app.on_startup.append(self.connect)
        app.on_cleanup.append(self.disconnect)

    async def connect(self, app: "Application"):
        return

    async def disconnect(self, app: "Application"):
        return

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator["AsyncSession"]:
        if not self.session_factory:
            raise RuntimeError("session_factory not set in accessor")
        async with self.session_factory() as session:
            yield session

    async def safe_execute(self, coro):
        try:
            return await coro
        except Exception as e:
            self.logger.error("DB operation failed: %s", str(e))
            raise
