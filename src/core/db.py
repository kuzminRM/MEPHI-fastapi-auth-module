from functools import wraps
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from src.core.config import settings

if TYPE_CHECKING:
    from typing import Any
    from typing import Callable

async_engine = create_async_engine(settings.SQLITE_CONNECTION_STRING, echo=settings.SQLITE_ECHO)
_async_session = async_sessionmaker(async_engine, expire_on_commit=False)


def db_session_as_kwarg(func: 'Callable') -> 'Callable':
    @wraps(func)
    async def wrapper(*args: 'Any', **kwargs: 'Any') -> 'Any':
        async with _async_session() as session:
            return await func(*args, **kwargs, session=session)

    return wrapper


async def session_di() -> 'Any':
    async with _async_session() as session:
        yield session
