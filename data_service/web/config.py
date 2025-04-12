import os
import typing
from dataclasses import dataclass

if typing.TYPE_CHECKING:
    from data_service.web.app import Application


@dataclass
class SessionConfig:
    key: str


@dataclass
class AdminConfig:
    email: str
    password: str


@dataclass
class DatabaseConfig:
    url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/course_db"


@dataclass
class Config:
    admin: AdminConfig
    session: SessionConfig | None = None
    database: DatabaseConfig | None = None


def setup_config(app: "Application"):
    app.config = Config(
        session=SessionConfig(
            key=os.getenv("SESSION_KEY"),
        ),
        admin=AdminConfig(
            email=os.getenv("ADMIN_EMAIL"),
            password=os.getenv("ADMIN_PASSWORD"),
        ),
        database=DatabaseConfig(os.getenv("POSTGRES_URL")),
    )
