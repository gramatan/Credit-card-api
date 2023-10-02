"""Конфигурация подключения к postgres."""
from dataclasses import dataclass


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
        login='shift_cc',
        password='shift_cc_pass',
        # host='cc_postgres',
        host='localhost',
        port='5432',
        db_name='shift_cc_db',
    ),
)
