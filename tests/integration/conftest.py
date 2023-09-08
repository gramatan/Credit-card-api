"""Конфтест для сценария интеграционных тестов."""
import io
from datetime import datetime
from decimal import Decimal

import pytest
from starlette.testclient import TestClient

from src.main import app
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


@pytest.fixture()
def good_client_with_token():
    """
    Фикстура получения хорошего токена.

    Returns:
        tuple[TestClient, dict]: Тестовый клиент и токен.
    """
    client = TestClient(app)
    response = client.post(
        url='api/auth',
        data={
            'username': 'test_user',
            'password': 'test_password',
        },
    )

    access_token = response.json()['access_token']
    token = {
        'Authorization': f'Bearer {access_token}',
    }

    return client, token


def prepare_files():
    """
    Подготовка файлов для тестов.

    Returns:
        tuple[io.BytesIO, io.BytesIO]: Подготовленные файлы.
    """
    selfie_stream = io.BytesIO(b'Nothing here')
    document_stream = io.BytesIO(b'Why do you read this?')

    selfie_stream.name = 'selfie.jpg'
    document_stream.name = 'document.jpg'

    return selfie_stream, document_stream
