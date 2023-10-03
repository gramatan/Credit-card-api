import asyncio

import asyncpg
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config.postgres_config import AppConfig, PostgresConfig
from credit_card_auth.src.database.base import Base

app_config = AppConfig(
    postgres=PostgresConfig(    # noqa: S106
        login='shift_cc',
        password='shift_cc_pass',
        host='localhost',
        port='5432',
        db_name='shift_cc_db_auth_test',
    ),
)


@pytest.fixture(scope='module')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='module')
async def config():
    app_config.postgres.db_name = f'{app_config.postgres.db_name}'
    print(f'метка = app_config=={app_config}')
    yield app_config


@pytest_asyncio.fixture(scope='module')
async def flush_db(config):
    postgres_table_uri = f'postgresql://{app_config.postgres.url}/postgres'

    connection = await asyncpg.connect(postgres_table_uri)
    await connection.execute(f'DROP DATABASE IF EXISTS {app_config.postgres.db_name}')
    await connection.execute(f'CREATE DATABASE {app_config.postgres.db_name}')
    await connection.close()


@pytest_asyncio.fixture(scope='module')
async def db_engine(config):
    yield create_async_engine(config.postgres.uri, echo=True)


@pytest_asyncio.fixture(scope='module')
async def new_db_schema(flush_db, db_engine):
    async with db_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    await db_engine.dispose()


@pytest_asyncio.fixture(scope='module')
async def db_session(new_db_schema, db_engine):
    pg_session = async_sessionmaker(db_engine, expire_on_commit=False)
    async with pg_session() as session:
        yield session
        await session.rollback()
        await session.close()
