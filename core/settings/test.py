import logging

from pydantic import AnyUrl
from pydantic import SecretStr

from core.settings.app import AppSettings


class TestAppSettings(AppSettings):
    debug: bool = True

    title: str = "Test FastAPI example app"

    secret_key: SecretStr = SecretStr("test_secret")

    logging_level: int = logging.DEBUG
