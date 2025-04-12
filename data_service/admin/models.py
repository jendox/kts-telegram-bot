from typing import Optional

from aiohttp_session import Session
from argon2 import PasswordHasher
from sqlalchemy.orm import Mapped

from data_service.admin.schemes import AdminSchema
from data_service.store.database.sqlalchemy_base import (
    BaseModel,
    prim_inc_an,
    uniq_str_an,
)


class Admin(BaseModel):
    __tablename__ = "admins"

    id: Mapped[prim_inc_an]
    email: Mapped[uniq_str_an]
    password: Mapped[str]

    def is_password_valid(self, password: str):
        return PasswordHasher().verify(hash=self.password, password=password)

    @staticmethod
    def hash_password(password: str) -> str:
        return PasswordHasher().hash(password)

    @classmethod
    def from_session(cls, session: Session) -> Optional["Admin"]:
        try:
            return cls(
                id=session["admin"]["id"], email=session["admin"]["email"]
            )
        except KeyError:
            return None

    def to_session(self, session: Session):
        session["admin"] = AdminSchema().dump(self)
