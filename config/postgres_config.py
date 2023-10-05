"""Конфигурация подключения к postgres."""
from dataclasses import dataclass

from config.config import (
    POSTGRES_DB_NAME,
    POSTGRES_DB_PASS,
    POSTGRES_DB_USER,
    POSTGRES_HOST,
    POSTGRES_PORT,
)


@dataclass
class PostgresConfig:
    """Конфигурация подключения к postgres."""

    login: str
    password: str
    host: str
    port: str
    db_name: str

    @property
    def url(self):
        """
        URL для подключения к postgres.

        Returns:
            str: URL для подключения к postgres.
        """
        creds = f'{self.login}:{self.password}'
        return f'{creds}@{self.host}:{self.port}'  # noqa: WPS221

    @property
    def uri(self):
        """
        URI для подключения к postgres.

        Returns:
            str: URI для подключения к postgres.
        """
        return f'postgresql+asyncpg://{self.url}/{self.db_name}'


@dataclass
class AppConfig:
    """Конфигурация приложения."""

    postgres: PostgresConfig


app_config = AppConfig(
    postgres=PostgresConfig(    # noqa: S106
        login=POSTGRES_DB_USER,
        password=POSTGRES_DB_PASS,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        db_name=POSTGRES_DB_NAME,
    ),
)
