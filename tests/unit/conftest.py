"""Набор фикстур для тестов."""
from decimal import Decimal
from datetime import datetime, timedelta

import pytest

from src.models.logs import BalanceLog, CommonLog
from src.repositories.log_storage import LogStorage
from src.repositories.user_storage import UserStorage


@pytest.fixture()
def not_empty_storage():
    """
    Фикстура для создания непустого хранилища.

    Yields:
        UserStorage: Хранилище c готовым пользователем.
    """
    storage = UserStorage()
    user_info = {'name': 'John'}
    card_number = '1234567890'
    storage.add(card_number, user_info)
    yield storage


@pytest.fixture(scope='function')
def log_storage_with_history():
    storage = LogStorage()
    base_date = datetime(year=2024, month=2, day=25)
    prev = Decimal(0)
    card_id = '1234567890'
    for i in range(10):
        log = BalanceLog(
            card_number=card_id,
            before=prev,
            after=prev + 100,
            changes=Decimal(100),
            _datetime_utc=base_date + timedelta(days=i)
        )
        storage.save(log)
        prev += 100
    yield storage


@pytest.fixture
def logs_collection():
    balance_logs = [
        BalanceLog(card_number='1234567890', before=Decimal(i * 100), after=Decimal((i + 1) * 100),
                   changes=Decimal(100))
        for i in range(5)
    ]

    common_logs = [
        CommonLog(card_number='1234567890', before=Decimal(i * 100), after=Decimal((i + 1) * 100), changes=Decimal(100))
        for i in range(3)
    ]

    return {
        'balance_logs': balance_logs,
        'common_logs': common_logs
    }
