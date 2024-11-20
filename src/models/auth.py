import datetime

from enum import StrEnum
from typing import Optional

from sqlalchemy import BigInteger
from sqlalchemy import Enum as SaEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from src.models.base import Base
from src.models.base import BaseNoId


class UserRolesEnum(StrEnum):
    ADMIN = 'admin'
    STAFF = 'staff'


class AuthUser(BaseNoId):
    __tablename__ = 'auth_user'

    username: Mapped[str] = mapped_column(primary_key=True)
    password: Mapped[str]

    updated_at: Mapped[datetime.datetime] = mapped_column(default=now(), onupdate=now())
    created_at: Mapped[datetime.datetime] = mapped_column(default=now())

    auth_user_roles_m2m: Mapped[list['AuthUserRolesM2M']] = relationship(back_populates='auth_user')

    def __repr__(self) -> str:
        return f'AuthUser(username={self.username}, auth_roles=[{[m2m.role for m2m in self.auth_user_roles_m2m]}])'


class AuthUserRolesM2M(Base):
    __tablename__ = 'auth_user_roles_m2m'
    auth_user_id: Mapped[str] = mapped_column(ForeignKey('auth_user.username', ondelete='CASCADE'))
    role: Mapped[UserRolesEnum]

    updated_at: Mapped[datetime.datetime] = mapped_column(default=now(), onupdate=now())
    created_at: Mapped[datetime.datetime] = mapped_column(default=now())

    auth_user: Mapped['AuthUser'] = relationship(back_populates='auth_user_roles_m2m')

    def __repr__(self) -> str:
        return f'AuthUserRoles(auth_user_id={self.auth_user_id}, role={self.role})'
