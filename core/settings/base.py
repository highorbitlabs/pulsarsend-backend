from enum import Enum

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

class AppEnvTypes(Enum):
    prod: str = "prod"
    dev: str = "dev"
    test: str = "test"


class BaseAppSettings(BaseSettings):
    app_env: AppEnvTypes = AppEnvTypes.prod

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
