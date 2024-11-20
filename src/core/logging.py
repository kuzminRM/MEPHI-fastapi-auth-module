import logging

from src.core.config import settings


def service_log() -> None:
    logging.basicConfig(level=logging.DEBUG if settings.DEBUG else logging.INFO)
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
