from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from src.auth.requires_roles import authenticate
from src.core.db import db_session_as_kwarg
from src.core.db import session_di
from src.models.auth import UserRolesEnum
from src.schemas.web.auth import AuthUserUsername
from src.schemas.web.roles_test_api import TestAuthOutput

router = APIRouter(
    tags=['Test Authorization Module'],
    prefix='/test_auth',
)


@router.get('/available_for_all', description='Доступно всем, даже не аутентифицированным пользователям')
async def available_for_all() -> TestAuthOutput:
    return TestAuthOutput(message='Доступно всем, даже не аутентифицированным пользователям')


@router.get('/available_for_authenticated', description='Доступно пользователям прошедшим аутентификацию')
async def available_for_authenticated(request: Request, session: Annotated[AsyncSession, Depends(session_di)]) -> TestAuthOutput:
    username: AuthUserUsername = await authenticate(request, session, [])
    return TestAuthOutput(message='Доступно пользователям прошедшим аутентификацию')


@router.get('/available_for_admin', description='Доступно пользователям с ролью "Администратор"')
async def available_for_admin(request: Request, session: Annotated[AsyncSession, Depends(session_di)]) -> TestAuthOutput:
    username: AuthUserUsername = await authenticate(request, session, [UserRolesEnum.ADMIN])
    return TestAuthOutput(message='Доступно пользователям с ролью "Администратор"')


@router.get('/available_for_stuff', description='Доступно пользователям с ролью "Сотрудник"')
async def available_for_stuff(request: Request, session: Annotated[AsyncSession, Depends(session_di)]) -> TestAuthOutput:
    username: AuthUserUsername = await authenticate(request, session, [UserRolesEnum.STAFF])
    return TestAuthOutput(message='Доступно пользователям с ролью "Сотрудник"')


@router.get('/available_for_admin_and_stuff', description='Доступно пользователям ролями "Сотрудник" и "Администратор"')
async def available_for_admin_and_stuff(request: Request, session: Annotated[AsyncSession, Depends(session_di)]) -> TestAuthOutput:
    username: AuthUserUsername = await authenticate(request, session, [UserRolesEnum.ADMIN, UserRolesEnum.STAFF])
    return TestAuthOutput(message='Доступно пользователям ролями "Сотрудник" и "Администратор"')
