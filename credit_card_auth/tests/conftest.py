import asyncio

import pytest
import pytest_asyncio
import asyncpg
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config.postgres_adaptor import get_db_session
from config.postgres_config import AppConfig, PostgresConfig
from credit_card_auth.src.database.base import Base
from main_auth import app

app_config = AppConfig(
    postgres=PostgresConfig(    # noqa: S106
        login='shift_cc',
        password='shift_cc_pass',
        host='localhost',
        port='5432',
        db_name='shift_cc_db_test',
    ),
)


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def config():
    app_config.postgres.db_name = f'{app_config.postgres.db_name}'
    print(f'метка = app_config=={app_config}')
    yield app_config


@pytest_asyncio.fixture(scope='session')
async def flush_db(config):
    postgres_table_uri = f'postgresql://{app_config.postgres.url}/postgres'

    connection = await asyncpg.connect(postgres_table_uri)
    await connection.execute(f'DROP DATABASE IF EXISTS {app_config.postgres.db_name}')
    await connection.execute(f'CREATE DATABASE {app_config.postgres.db_name}')
    await connection.close()


@pytest_asyncio.fixture(scope='session')
async def db_engine(config):
    yield create_async_engine(config.postgres.uri, echo=True)


@pytest_asyncio.fixture(scope='session')
async def new_db_schema(flush_db, db_engine):
    async with db_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    await db_engine.dispose()


@pytest_asyncio.fixture(scope='session')
async def db_session(new_db_schema, db_engine):
    pg_session = async_sessionmaker(db_engine, expire_on_commit=False)
    async with pg_session() as session, session.begin():
        yield session
        await session.rollback()
        await session.close()


@pytest_asyncio.fixture()
async def test_client() -> AsyncClient:  # type: ignore
    app.dependency_overrides[get_db_session] = db_session
    async with AsyncClient(app=app, base_url='https://localhost:24001') as client:
        yield client
        await client.aclose()
