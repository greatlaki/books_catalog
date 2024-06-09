import logging
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger('app')
ENV_FILE = Path.cwd() / '.env'


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix='ENV_POSTGRES_',
        extra='ignore',
    )

    USER: str
    PASSWORD: str
    HOST: str
    PORT: int
    NAME: str

    @property
    def ADDRESS(self) -> str:
        return f'postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}'


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix='APP_',
        extra='ignore',
    )

    PREFIX: str = '/backend'

    PG: PostgresSettings = PostgresSettings()


settings: AppSettings = AppSettings()
