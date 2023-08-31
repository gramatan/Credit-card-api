"""Набор фикстур для тестов."""
from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from src.models.logs import BalanceLog, CommonLog
from src.repositories.log_storage import LogStorage
from src.repositories.user_storage import UserStorage

CARD_ID = '1234567890'


@pytest.fixture()
def not_empty_storage():
    """
    Фикстура для создания непустого хранилища.

    Yields:
        UserStorage: Хранилище c готовым пользователем.
    """
    storage = UserStorage()
    user_info = {'name': 'John'}
    storage.add(CARD_ID, user_info)
    yield storage


@pytest.fixture(scope='function')
def log_storage_with_history():
    """
    Фикстура для создания хранилища с историей.

    Yields:
        LogStorage: Хранилище с историей.
    """
    storage = LogStorage()
    base_date = datetime(year=2024, month=2, day=25)
    prev = Decimal(0)
    for addtional_day in range(10):
        log = BalanceLog(
            card_number=CARD_ID,
            before=prev,
            after=prev + 100,
            changes=Decimal(100),
            _datetime_utc=base_date + timedelta(days=addtional_day),
        )
        storage.save(log)
        prev += 100
    yield storage


@pytest.fixture
def logs_collection():
    """
    Фикстура для создания коллекции логов.

    Returns:
        dict: Коллекция логов.
    """
    balance_logs = [
        BalanceLog(
            card_number=CARD_ID,
            before=Decimal(index * 100),
            after=Decimal((index + 1) * 100),
            changes=Decimal(100),
        )
        for index in range(5)
    ]

    common_logs = [
        CommonLog(
            card_number=CARD_ID,
            before=Decimal(index * 100),
            after=Decimal((index + 1) * 100),
            changes=Decimal(100),
        )
        for index in range(3)
    ]

    return {
        'balance_logs': balance_logs,
        'common_logs': common_logs,
    }
