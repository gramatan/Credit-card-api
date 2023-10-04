"""Набор фикстур для тестов."""
import asyncio

import asyncpg
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config.config import POSTGRES_HOST
from config.postgres_config import AppConfig, PostgresConfig
from credit_card_auth.src.database.base import Base

app_config = AppConfig(
    postgres=PostgresConfig(    # noqa: S106
        login='shift_cc',
        password='shift_cc_pass',
        host=POSTGRES_HOST,
        port='5432',
        db_name='shift_cc_db_auth_test',
    ),
)

@pytest.fixture(scope='module')
def event_loop():
    """
    Фикстура для создания цикла событий.

    Yields:
        asyncio.AbstractEventLoop: Цикл событий.
    """
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='module')
async def config():
    """
    Фикстура для создания конфигурации приложения.

    Yields:
        AppConfig: Конфигурация приложения.
    """
    app_config.postgres.db_name = f'{app_config.postgres.db_name}'
    yield app_config


@pytest_asyncio.fixture(scope='module')
async def flush_db(config):
    """
    Фикстура для подготовки БД.

    Args:
        config: Конфигурация приложения.
    """
    postgres_table_uri = f'postgresql://{app_config.postgres.url}/postgres'

    connection = await asyncpg.connect(postgres_table_uri)
    await connection.execute(f'DROP DATABASE IF EXISTS {app_config.postgres.db_name}')  # noqa: E501
    await connection.execute(f'CREATE DATABASE {app_config.postgres.db_name}')
    await connection.close()


@pytest_asyncio.fixture(scope='module')
async def db_engine(config):
    """
    Фикстура для создания движка БД.

    Args:
        config: Конфигурация приложения.

    Yields:
        Engine: Подключение к БД.
    """
    yield create_async_engine(config.postgres.uri, echo=True)


@pytest_asyncio.fixture(scope='module')
async def new_db_schema(flush_db, db_engine):
    """
    Фикстура для создания схемы БД.

    Args:
        flush_db: Фикстура для подготовки БД.
        db_engine: Фикстура для создания движка БД.

    Yields:
        None
    """
    async with db_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    await db_engine.dispose()


@pytest_asyncio.fixture(scope='module')
async def db_session(new_db_schema, db_engine):
    """
    Фикстура для создания сессии БД.

    Args:
        new_db_schema: Фикстура для создания схемы БД.
        db_engine: Фикстура для создания движка БД.

    Yields:
        Session: Сессия БД.
    """
    pg_session = async_sessionmaker(db_engine, expire_on_commit=False)
    async with pg_session() as session:
        yield session
        await session.rollback()
        await session.close()
