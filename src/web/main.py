from fastapi import FastAPI
from fastapi import Request
from starlette.responses import JSONResponse

from src.core.config import settings
from src.exeptions.base import BaseError
from src.schemas.web.error import Error
from src.schemas.web.error import ErrorContainer
from src.web.routers.roles_test import router as roles_test_router

fastapi_app = FastAPI(
    title=settings.SERVICE_NAME,
    root_path=settings.ROOT_PATH,
)

fastapi_app.include_router(roles_test_router)


@fastapi_app.middleware('http')
async def error_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
    except BaseError as e:
        response = JSONResponse(
            content=ErrorContainer(error=Error(message=e.message, code=e.code)).dict(),
            status_code=e.http_code,
        )
    return response


@fastapi_app.get('/ping', tags=['Service'])
def ping() -> dict:
    return {'message': 'pong'}
