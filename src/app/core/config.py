import os
from enum import Enum

from pydantic_settings import BaseSettings
from starlette.config import Config

current_file_dir = os.path.dirname(os.path.realpath(__file__))
env_path = os.path.join(current_file_dir, "..", "..", ".env")
config = Config(env_path)


class AppSettings(BaseSettings):
    APP_NAME: str = config("APP_NAME", default="Dothe2")
    APP_DESCRIPTION: str | None = config("APP_DESCRIPTION", default=None)
    APP_VERSION: str | None = config("APP_VERSION", default=None)
    LICENSE_NAME: str | None = config("LICENSE", default=None)
    CONTACT_NAME: str | None = config("CONTACT_NAME", default=None)
    CONTACT_EMAIL: str | None = config("CONTACT_EMAIL", default=None)


class DatabaseSettings(BaseSettings):
    pass


class PostgresSettings(DatabaseSettings):
    POSTGRES_USER: str = config("POSTGRES_USER", default="postgres")
    POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", default="postgres")
    POSTGRES_SERVER: str = config("POSTGRES_SERVER", default="localhost")
    POSTGRES_PORT: int = config("POSTGRES_PORT", default=5432)
    POSTGRES_DB: str = config("POSTGRES_DB", default="postgres")
    POSTGRES_SYNC_PREFIX: str = config("POSTGRES_SYNC_PREFIX", default="postgresql://")
    POSTGRES_ASYNC_PREFIX: str = config("POSTGRES_ASYNC_PREFIX", default="postgresql+asyncpg://")
    POSTGRES_URI: str = f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    POSTGRES_URL: str | None = config("POSTGRES_URL", default=None)


class EnvironmentOption(Enum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"


class EnvironmentSettings(BaseSettings):
    ENVIRONMENT: EnvironmentOption = config("ENVIRONMENT", default="local")


class EmailSettings(BaseSettings):
    EMAIL_HOST: str = config("EMAIL_HOST", default="smtp.gmail.com")
    EMAIL_PORT: int = config("EMAIL_PORT", default=587)
    EMAIL_USERNAME: str = config("EMAIL_USERNAME", default="")
    EMAIL_PASSWORD: str = config("EMAIL_PASSWORD", default="")
    EMAIL_FROM_ADDRESS: str = config("EMAIL_FROM_ADDRESS", default="noreply@dothe2.app")
    EMAIL_FROM_NAME: str = config("EMAIL_FROM_NAME", default="Dothe2")
    EMAIL_USE_TLS: bool = config("EMAIL_USE_TLS", default=True)
    EMAIL_USE_SSL: bool = config("EMAIL_USE_SSL", default=False)


class AuthSettings(BaseSettings):
    SECRET_KEY: str = config("SECRET_KEY", default="your-secret-key-here-change-in-production")
    ALGORITHM: str = config("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=60 * 24 * 7)  # 7 days
    MAGIC_LINK_EXPIRE_MINUTES: int = config("MAGIC_LINK_EXPIRE_MINUTES", default=15)
    BASE_URL: str = config("BASE_URL", default="http://localhost:8000")


class Settings(
    AppSettings,
    PostgresSettings,
    EnvironmentSettings,
    EmailSettings,
    AuthSettings,
):
    pass


settings = Settings()
