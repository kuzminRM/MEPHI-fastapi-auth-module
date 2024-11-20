from sqlalchemy import Result
from sqlalchemy import ScalarResult
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import AuthUser
from src.models import AuthUserRolesM2M
from src.models.auth import UserRolesEnum
from src.schemas.web.auth import AuthUserUsername


async def authenticate_user_with_roles(
        username: str, password: str, roles: list[UserRolesEnum], session: AsyncSession,
) -> AuthUserUsername | None:
    request: ScalarResult = await session.scalars(
        select(AuthUser)
        .join(AuthUserRolesM2M, AuthUserRolesM2M.auth_user_id == AuthUser.username)
        .where(AuthUser.username == username)
        .where(AuthUser.password == password)
        .where(AuthUserRolesM2M.role.in_(roles))
        .limit(1),
    )
    result = request.one_or_none()
    return result.username if result else None


async def authenticate_user(
        username: str, password: str, session: AsyncSession,
) -> AuthUserUsername | None:
    request: ScalarResult = await session.scalars(
        select(AuthUser)
        .where(AuthUser.username == username)
        .where(AuthUser.password == password)
        .limit(1),
    )
    result = request.one_or_none()
    return result.username if result else None
