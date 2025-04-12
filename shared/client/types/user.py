from dataclasses import dataclass

__all__ = ("User",)


@dataclass
class User:
    id: int
    is_bot: bool
    first_name: str
    last_name: str | None = None
    username: str | None = None
