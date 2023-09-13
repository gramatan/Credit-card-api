"""Тесты эндпоинтов роутера баланса."""
from datetime import datetime
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from main_balance import app


@pytest.mark.parametrize('card_number, expected', [
    pytest.param('123', True, id='normal card number'),
])
def test_balance(card_number, expected):
    """
    Тест на баланс.

    Args:
        card_number (str): Номер карты.
        expected (bool): Ожидаемый результат.
    """
    client = TestClient(app)
    response = client.get(
        url='api/balance',
        params={
            'card_number': card_number,
        },
    )
    assert response.status_code == 200
    assert response.json()['card_number'] == card_number
    assert 'balance' in response.json()


@pytest.mark.parametrize('card_number, depos, withdrawals', [
    pytest.param('123', 1, 0, id='1 depo, 0 withdrawals'),
    pytest.param('123', 1, 1, id='1 depo, 1 withdrawals'),
    pytest.param('123', 10, 10, id='10 depo, 10 withdrawals'),
    pytest.param('123', 5, 3, id='5 depo, 3 withdrawals'),
])
def test_balance_story(
    card_number,
    depos,
    withdrawals,
):
    """
    Тест на историю баланса.

    Args:
        card_number (str): Номер карты.
        depos (int): Количество депозитов.
        withdrawals (int): Количество снятий.
    """
    client = TestClient(app)

    start_length = client.get(
        url='api/balance/history',
        params={
            'card_number': card_number,
            'from_date': datetime(1970, 1, 1),
            'to_date': datetime(3000, 1, 1),
        },
    ).json()

    for _ in range(depos):
        client.post(
            url='api/deposit',
            params={
                'card_number': '123',
                'amount': Decimal(100),
            },
        )

    for _ in range(withdrawals):
        client.post(
            url='api/withdrawal',
            params={
                'card_number': '123',
                'amount': Decimal(100),
            },
        )

    response = client.get(
        url='api/balance/history',
        params={
            'card_number': card_number,
            'from_date': datetime(1970, 1, 1),
            'to_date': datetime(3000, 1, 1),
        },
    )
    expected_length = depos + withdrawals + len(start_length)
    assert response.status_code == 200
    assert len(response.json()) == expected_length
