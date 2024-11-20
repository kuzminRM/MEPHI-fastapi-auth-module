from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class BaseNoId(DeclarativeBase):
    pass


class Base(BaseNoId):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
