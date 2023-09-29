from dataclasses import dataclass


@dataclass
class PostgresConfig:
    login: str
    password: str
    host: str
    port: str
    db_name: str

    @property
    def url(self):
        return f'{self.login}:{self.password}@{self.host}:{self.port}'

    @property
    def uri(self):
        return f'postgresql+asyncpg://{self.url}/{self.db_name}'


@dataclass
class AppConfig:
    postgres: PostgresConfig


app_config = AppConfig(
    postgres=PostgresConfig(
        login='shift_cc',
        password='shift_cc_pass',
        host='127.0.0.1',
        port='5432',
        db_name='shift_cc_db',
    ),
)
