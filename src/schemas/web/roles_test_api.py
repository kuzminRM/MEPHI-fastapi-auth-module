from __future__ import annotations

from pydantic import BaseModel

from src.schemas.web.error import ErrorContainer


class TestAuthOutput(ErrorContainer):
    message: str
