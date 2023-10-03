"""Фикстуры для тестов."""
import asyncio
from datetime import datetime, timedelta

import asyncpg
import pytest
import pytest_asyncio
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config.config import POSTGRES_HOST
from config.postgres_config import AppConfig, PostgresConfig
from credit_card_balance.src.database.base import (
    BalanceLogAlchemyModel,
    Base,
    CardAlchemyModel,
)

app_config = AppConfig(
    postgres=PostgresConfig(    # noqa: S106
        login='shift_cc',
        password='shift_cc_pass',
        host=POSTGRES_HOST,
        port='5432',
        db_name='shift_cc_db_balance_test',
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
    Фикстура для очистки БД.

    Args:
        config: конфигурация приложения
    """
    postgres_table_uri = f'postgresql://{app_config.postgres.url}/postgres'

    connection = await asyncpg.connect(postgres_table_uri)
    await connection.execute(f'DROP DATABASE IF EXISTS {app_config.postgres.db_name}')  # noqa: E501
    await connection.execute(f'CREATE DATABASE {app_config.postgres.db_name}')
    await connection.close()


@pytest_asyncio.fixture(scope='module')
async def db_engine(config):
    """
    Фикстура для создания подключения к БД.

    Args:
        config: конфигурация приложения

    Yields:
        Engine: Подключение к БД.
    """
    yield create_async_engine(config.postgres.uri, echo=True)


@pytest_asyncio.fixture(scope='module')
async def new_db_schema(flush_db, db_engine):
    """
    Фикстура для создания схемы БД.

    Args:
        flush_db: фикстура для очистки БД
        db_engine: фикстура для подключения к БД

    Yields:
        None
    """
    async with db_engine.begin() as first_connection:
        await first_connection.run_sync(Base.metadata.drop_all)

    async with db_engine.begin() as second_connection:
        await second_connection.run_sync(Base.metadata.create_all)
    yield
    await db_engine.dispose()


@pytest_asyncio.fixture(scope='module')
async def db_session(new_db_schema, db_engine):
    """
    Фикстура для создания сессии для работы с БД.

    Args:
        new_db_schema: фикстура для создания схемы БД
        db_engine: фикстура для подключения к БД

    Yields:
        AsyncSession: Сессия для работы с БД.
    """
    pg_session = async_sessionmaker(db_engine, expire_on_commit=False)
    async with pg_session() as session:
        yield session
        await session.rollback()
        await session.close()


@pytest_asyncio.fixture(autouse=True)
async def prepare_cards_for_logs(db_engine):
    """
    Фикстура для подготовки карт.

    Args:
        db_engine: фикстура для подключения к БД

    Yields:
        None
    """
    cards = [
        CardAlchemyModel(
            card_number='123',
            card_limit=1000,
            card_balance=0,
            card_first_name='Ivan',
        ),
        CardAlchemyModel(
            card_number='456',
            card_limit=0,
            card_balance=0,
        ),
        CardAlchemyModel(
            card_number='789',
            card_limit=0,
            card_balance=0,
        ),
    ]

    async with async_sessionmaker(bind=db_engine)() as session:
        try:                                # noqa: WPS229
            for card in cards:
                session.add(card)
            await session.commit()
            await session.close()
        except IntegrityError:
            print('Cards already exist')    # noqa: WPS421
    yield


@pytest_asyncio.fixture(autouse=True)
async def prepare_balance_logs(   # noqa: WPS210
    prepare_cards_for_logs,
    db_engine,
):
    """
    Фикстура для подготовки логов баланса.

    Args:
        prepare_cards_for_logs: фикстура для подготовки карт
        db_engine: фикстура для подключения к БД

    Yields:
        None
    """
    async with async_sessionmaker(bind=db_engine)() as session:
        base_date = datetime(year=2024, month=2, day=25)
        prev = 0
        logs = []
        for addtional_day in range(10):
            log = BalanceLogAlchemyModel(
                card_number_id=2,
                balance_before=prev,
                balance_after=prev + 1000,
                changes=1000,
                datetime_utc=base_date + timedelta(days=addtional_day),
            )
            prev += 1000
            logs.append(log)
        try:        # noqa: WPS229
            session.add_all(logs)
            await session.commit()
            await session.close()
        except IntegrityError:
            print('Logs already exist')     # noqa: WPS421
    yield
