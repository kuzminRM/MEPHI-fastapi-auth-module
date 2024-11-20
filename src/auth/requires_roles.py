from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from src.dao.auth.auth_user import authenticate_user
from src.dao.auth.auth_user import authenticate_user_with_roles
from src.exeptions.auth import AuthenticationError
from src.exeptions.auth import AuthHeaderRequired
from src.models.auth import AuthUser
from src.models.auth import UserRolesEnum
from src.schemas.web.auth import AuthUserUsername


async def authenticate(request: Request, session: AsyncSession, roles: list[UserRolesEnum]) -> AuthUserUsername:
    header_data: str | None = request.headers.get('Authorization')
    if header_data is None:
        raise AuthHeaderRequired

    username, password = header_data.split(':')
    username_from_db: AuthUserUsername | None
    if roles:
        username_from_db = await authenticate_user_with_roles(username, password, roles, session)
    else:
        username_from_db = await authenticate_user(username, password, session)

    if username_from_db is None:
        raise AuthenticationError

    return username_from_db
