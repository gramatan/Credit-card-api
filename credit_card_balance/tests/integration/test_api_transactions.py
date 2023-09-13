"""Тесты эндпоинтов роутера транзакций."""
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from main_balance import app


@pytest.mark.parametrize('deposit_sum, expected', [
    pytest.param(Decimal(100), True, id='normal sum'),
    pytest.param(Decimal(0), False, id='Zero sum'),
    pytest.param(Decimal(-100), False, id='negative sum'),
    pytest.param(Decimal(1000000000000), True, id='big depo'),
    pytest.param(Decimal(100.998), True, id='decimal'),
])
def test_deposit(deposit_sum, expected):
    """
    Тест на депозит.

    Args:
        deposit_sum (Decimal): Сумма депозита.
        expected (bool): Ожидаемый результат.
    """
    client = TestClient(app)
    if not expected:    # noqa: WPS504
        with pytest.raises(ValueError):
            client.post(
                url='api/deposit',
                params={
                    'card_number': '123',
                    'amount': deposit_sum,
                },
            )
    else:
        response = client.post(
            url='api/deposit',
            params={
                'card_number': '123',
                'amount': deposit_sum,
            },
        )
        cur_bal = Decimal(response.json()['balance'])

        response = client.post(
            url='api/deposit',
            params={
                'card_number': '123',
                'amount': deposit_sum,
            },
        )
        expected_balance = cur_bal + deposit_sum

        assert response.status_code == 200
        assert response.json()['card_number'] == '123'
        assert response.json()['balance'] == str(expected_balance)


@pytest.mark.parametrize('withdraw_sum, expected', [
    pytest.param(Decimal(100), True, id='normal sum'),
    pytest.param(Decimal(0), False, id='Zero sum'),
    pytest.param(Decimal(-100), False, id='negative sum'),
    pytest.param(Decimal(100.99), True, id='decimal'),
    pytest.param(
        Decimal(1000000000000),
        True,
        id='More than you(but not our user) have',
    ),
])
def test_withdrawal(withdraw_sum, expected):
    """
    Тест на снятие.

    Args:
        withdraw_sum (Decimal): Сумма снятия.
        expected (bool): Ожидаемый результат.
    """
    client = TestClient(app)

    if not expected:    # noqa: WPS504
        with pytest.raises(ValueError):
            client.post(
                url='api/deposit',
                params={
                    'card_number': '123',
                    'amount': withdraw_sum,
                },
            )
    else:
        response = client.post(
            url='api/withdrawal',
            params={
                'card_number': '123',
                'amount': withdraw_sum,
            },
        )
        cur_bal = Decimal(response.json()['balance'])

        response = client.post(
            url='api/withdrawal',
            params={
                'card_number': '123',
                'amount': withdraw_sum,
            },
        )
        expected_balance = cur_bal - withdraw_sum

        assert response.status_code == 200
        assert response.json()['card_number'] == '123'
        assert response.json()['balance'] == str(expected_balance)
