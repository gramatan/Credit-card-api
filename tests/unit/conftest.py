"""Набор фикстур для тестов."""
from datetime import datetime, timedelta
from decimal import Decimal

import jwt
import pytest

from config.config import ALGORITHM, SECRET_KEY
from src.models.logs import BalanceLog, CommonLog
from src.models.user import User
from src.repositories.log_storage import LogStorage
from src.repositories.transactions import Transactions
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
    storage.add(
        card_number=CARD_ID,
        user_info=user_info,
    )
    storage.update_user(User(
        CARD_ID,
        _balance=Decimal(0),
        limit=Decimal(1000),
        info=user_info,
    ))
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
            _datetime_utc=datetime.utcnow(),
        )
        for index in range(5)
    ]

    common_logs = [
        CommonLog(
            card_number=CARD_ID,
            before=Decimal(index * 100),
            after=Decimal((index + 1) * 100),
            changes=Decimal(100),
            _datetime_utc=datetime.utcnow(),
        )
        for index in range(3)
    ]

    return {
        'balance_logs': balance_logs,
        'common_logs': common_logs,
    }


@pytest.fixture
def transactions_fixture(not_empty_storage):    # noqa: WPS442
    """
    Фикстура для создания транзакций.

    Args:
        not_empty_storage (UserStorage): Хранилище с готовым пользователем.

    Yields:
        Transactions: Объект транзакций.
    """
    yield Transactions(not_empty_storage, LogStorage())


@pytest.fixture
def valid_token_data():
    """
    Валидные данные для токена.

    Returns:
        dict: Данные для токена.
    """
    return {'sub': 'test_user'}


def create_token(token_data: dict, token_type: str):
    """
    Создание токена.

    Args:
        token_data (dict): Данные для токена.
        token_type (str): Тип токена.

    Returns:
        str: Токен.
    """
    if token_type == 'expired':
        exp = datetime.utcnow() - timedelta(minutes=1)
        token_data = {**token_data, 'exp': exp}

    if token_type == 'wrong_secret_key':
        return jwt.encode(token_data, 'wrong_secret_key', algorithm=ALGORITHM)

    if token_type == 'no_sub_field':
        token_data = {'data': 'no_sub_field'}

    return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
