from typing import Annotated

from sqlalchemy.orm import DeclarativeBase, mapped_column

uniq_str_an = Annotated[str, mapped_column(unique=True)]
prim_inc_an = Annotated[
    int, mapped_column(primary_key=True, autoincrement=True)
]


class BaseModel(DeclarativeBase):
    __abstract__ = True
