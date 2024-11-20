import os

import pytest_asyncio

from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from src.core.db import session_di
from src.models.base import BaseNoId
from src.web.main import fastapi_app


@pytest_asyncio.fixture(name='session', loop_scope='module')
async def session_fixture():
    engine = create_engine('sqlite:///test.db', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    BaseNoId.metadata.create_all(engine)

    async_engine = create_async_engine('sqlite+aiosqlite:///test.db', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    async with AsyncSession(async_engine) as session:
        yield session

    BaseNoId.metadata.drop_all(engine)
    os.remove('test.db')


@pytest_asyncio.fixture(name='client', loop_scope='module')
async def client_fixture(session: AsyncSession):
    def get_session_override():
        return session

    fastapi_app.dependency_overrides[session_di] = get_session_override

    client = TestClient(fastapi_app)
    yield client
    fastapi_app.dependency_overrides.clear()
