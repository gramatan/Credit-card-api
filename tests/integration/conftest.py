"""Конфтест для сценария интеграционных тестов."""
from datetime import datetime
from decimal import Decimal

import pytest

from src.models.logs import BalanceLog
from src.repositories.log_storage import LogStorage
from src.repositories.transactions import Transactions
from src.repositories.user_storage import UserStorage


@pytest.fixture(scope='module')
def transaction_repo():
    """
    Фикстура для создания репо с хранилищами на сессию.

    Yields:
        Transactions: Репозиторий транзакций.
    """
    log_storage = LogStorage()
    user_storage = UserStorage()
    transaction_repo = Transactions(    # noqa: WPS442
        user_storage=user_storage,
        history=log_storage,
    )
    yield transaction_repo


@pytest.fixture
def user_data():
    """
    Фикстура для создания данных пользователя.

    Returns:
        dict: Данные для тестов.
    """
    return {
        'card_number': '8675309321679911',
        'create_user': {
            'info': {'name': 'John Doe', 'phone': '1234567890'},
        },
        'increase_limit': {
            'amount': Decimal('1000.0'),
        },
        'deposit': {
            'amount': Decimal('100.0'),
            'expected_balance': Decimal('100.0'),
        },
        'withdraw': {
            'amount': Decimal('120.0'),
            'expected_balance': Decimal('-20.0'),
        },
        'get_balance_log': {
            'length': 2,
            'expected_list': [BalanceLog(
                card_number='8675309321679911',
                before=Decimal('0'),
                after=Decimal('100'),
                changes=Decimal('100'),
                _datetime_utc=datetime.utcnow(),
            ), BalanceLog(
                card_number='8675309321679911',
                before=Decimal('100'),
                after=Decimal('-20'),
                changes=Decimal('-120'),
                _datetime_utc=datetime.utcnow(),
            )],
        },
    }
