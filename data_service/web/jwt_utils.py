import enum
import os

from jose import JWTError, jwt
from jose.constants import ALGORITHMS

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")


class UserRole(enum.Enum):
    ADMIN = "admin"
    BOT = "bot"


def decode_jwt(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHMS.HS256])
    except JWTError:
        return None
