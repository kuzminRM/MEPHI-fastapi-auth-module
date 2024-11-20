import pytest

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import AuthUser
from src.models import AuthUserRolesM2M
from src.models.auth import UserRolesEnum


async def create_test_data(session: AsyncSession):
    session.add(c := AuthUser(username='common_user', password='1'))
    session.add(a := AuthUser(username='admin_user', password='2'))
    session.add(s := AuthUser(username='staff_user', password='3'))
    session.add(AuthUserRolesM2M(auth_user=a, role=UserRolesEnum.ADMIN))
    session.add(AuthUserRolesM2M(auth_user=a, role=UserRolesEnum.STAFF))
    session.add(AuthUserRolesM2M(auth_user=s, role=UserRolesEnum.STAFF))
    await session.commit()


@pytest.mark.asyncio(loop_scope='module')
async def test_available_for_all(session: AsyncSession, client: TestClient):
    await create_test_data(session)
    TEST_URL = '/test_auth/available_for_all'

    response = client.get(TEST_URL)
    assert response.status_code == 200
    response = client.get(TEST_URL, headers={'Authorization': 'unknown_user:0'})
    assert response.status_code == 200
    response = client.get(TEST_URL, headers={'Authorization': 'common_user:wrong_pass'})
    assert response.status_code == 200
    response = client.get(TEST_URL, headers={'Authorization': 'common_user:1'})
    assert response.status_code == 200
    response = client.get(TEST_URL, headers={'Authorization': 'admin_user:2'})
    assert response.status_code == 200
    response = client.get(TEST_URL, headers={'Authorization': 'staff_user:3'})
    assert response.status_code == 200


@pytest.mark.asyncio(loop_scope='module')
async def test_available_for_authenticated(session: AsyncSession, client: TestClient):
    await create_test_data(session)
    TEST_URL = '/test_auth/available_for_authenticated'

    response = client.get(TEST_URL)
    assert response.status_code == 403
    response = client.get(TEST_URL, headers={'Authorization': 'unknown_user:0'})
    assert response.status_code == 403
    response = client.get(TEST_URL, headers={'Authorization': 'common_user:wrong_pass'})
    assert response.status_code == 403
    response = client.get(TEST_URL, headers={'Authorization': 'common_user:1'})
    assert response.status_code == 200
    response = client.get(TEST_URL, headers={'Authorization': 'admin_user:2'})
    assert response.status_code == 200
    response = client.get(TEST_URL, headers={'Authorization': 'staff_user:3'})
    assert response.status_code == 200


@pytest.mark.asyncio(loop_scope='module')
async def test_available_for_admin(session: AsyncSession, client: TestClient):
    await create_test_data(session)
    TEST_URL = '/test_auth/available_for_admin'

    response = client.get(TEST_URL)
    assert response.status_code == 403
    response = client.get(TEST_URL, headers={'Authorization': 'unknown_user:0'})
    assert response.status_code == 403
    response = client.get(TEST_URL, headers={'Authorization': 'common_user:wrong_pass'})
    assert response.status_code == 403
    response = client.get(TEST_URL, headers={'Authorization': 'common_user:1'})
    assert response.status_code == 403
    response = client.get(TEST_URL, headers={'Authorization': 'admin_user:2'})
    assert response.status_code == 200
    response = client.get(TEST_URL, headers={'Authorization': 'staff_user:3'})
    assert response.status_code == 403


@pytest.mark.asyncio(loop_scope='module')
async def test_available_for_stuff(session: AsyncSession, client: TestClient):
    await create_test_data(session)
    TEST_URL = '/test_auth/available_for_stuff'

    response = client.get(TEST_URL)
    assert response.status_code == 403
    response = client.get(TEST_URL, headers={'Authorization': 'unknown_user:0'})
    assert response.status_code == 403
    response = client.get(TEST_URL, headers={'Authorization': 'common_user:wrong_pass'})
    assert response.status_code == 403
    response = client.get(TEST_URL, headers={'Authorization': 'common_user:1'})
    assert response.status_code == 403
    response = client.get(TEST_URL, headers={'Authorization': 'admin_user:2'})
    assert response.status_code == 200
    response = client.get(TEST_URL, headers={'Authorization': 'staff_user:3'})
    assert response.status_code == 200


@pytest.mark.asyncio(loop_scope='module')
async def test_available_for_admin_and_stuff(session: AsyncSession, client: TestClient):
    await create_test_data(session)
    TEST_URL = '/test_auth/available_for_admin_and_stuff'

    response = client.get(TEST_URL)
    assert response.status_code == 403
    response = client.get(TEST_URL, headers={'Authorization': 'unknown_user:0'})
    assert response.status_code == 403
    response = client.get(TEST_URL, headers={'Authorization': 'common_user:wrong_pass'})
    assert response.status_code == 403
    response = client.get(TEST_URL, headers={'Authorization': 'common_user:1'})
    assert response.status_code == 403
    response = client.get(TEST_URL, headers={'Authorization': 'admin_user:2'})
    assert response.status_code == 200
    response = client.get(TEST_URL, headers={'Authorization': 'staff_user:3'})
    assert response.status_code == 200
