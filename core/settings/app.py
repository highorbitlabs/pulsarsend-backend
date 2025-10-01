import logging
import sys
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from loguru import logger
from pydantic import AnyUrl
from pydantic import AnyHttpUrl
from pydantic import Field

from core.logging import InterceptHandler
from core.settings.base import BaseAppSettings


class PostgresDsn(AnyUrl):
    allowed_schemes = {'postgres', 'postgresql', 'postgresql+asyncpg'}
    user_required = True


class AppSettings(BaseAppSettings):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "FastAPI example app"
    version: str = "0.0.0"

    ROOT_PATH: str = ''
    # POSTGRES_ASYNC_URL: PostgresDsn
    # POSTGRES_URL: PostgresDsn
    # SQLALCHEMY_DATABASE_URI: PostgresDsn

    # POSTGRES_USER: str = "user"
    # POSTGRES_PASSWORD: str = "password"
    # POSTGRES_HOST: str = "localhost"
    # POSTGRES_PORT: str = "5432"
    # POSTGRES_DB: str = "backoffice_auth_db"

    ACCESS_TOKEN_SECRET_KEY: str
    ALGORITHM: str

    PRIVY_APP_ID: str
    PRIVY_APP_SECRET: str
    PRIVY_API_BASE_URL: AnyHttpUrl = Field(default="https://api.privy.io")
    PRIVY_API_TIMEOUT_SECONDS: float = Field(default=10.0, ge=0.1)
    PRIVY_JWT_VERIFICATION_KEY_PEM: str
    
    SUPABASE_ID: str
    SUPABASE_KEY: str
    SUPABASE_DB_CODE: str

    api_prefix: str = "/api"

    jwt_token_prefix: str = "Token"

    allowed_hosts: List[str] = ["*"]

    logging_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    class Config:
        validate_assignment = True

    def get_database_url(self) -> str:
        return (
            f"postgresql://postgres.{self.SUPABASE_ID}:{self.SUPABASE_DB_CODE}@aws-1-eu-central-1.pooler.supabase.com:5432/postgres"    
            )

    def get_async_database_url(self) -> str:
        return (
            f"postgresql+asyncpg://postgres.{self.SUPABASE_ID}:{self.SUPABASE_DB_CODE}@aws-1-eu-central-1.pooler.supabase.com:5432/postgres"
        )

    def get_sqlalchemy_database_uri(self) -> str:
        return str(self.SQLALCHEMY_DATABASE_URI)

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
            "root_path": self.ROOT_PATH
        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level}])
