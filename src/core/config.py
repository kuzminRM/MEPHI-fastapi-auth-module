from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = 'FastAPI auth module'
    ROOT_PATH: str = ''
    API_HOST: str = 'localhost'
    API_PORT: int = 8000
    API_WORKERS: int = 1
    API_ALLOW_IPS: str = '*'
    DEBUG: bool = False

    SQLITE_DB: str = 'fast_api_auth.sqlite'
    SQLITE_ECHO: bool = False

    @property
    def SQLITE_CONNECTION_STRING(self) -> str:
        return f'sqlite+aiosqlite:///{self.SQLITE_DB}'

    @property
    def ALEMBIC_CONNECTION_STRING(self) -> str:
        return f'sqlite:///{self.SQLITE_DB}'


settings = Settings(_env_file='.env')  # type: ignore[call-arg]
