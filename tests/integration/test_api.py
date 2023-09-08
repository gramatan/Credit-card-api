"""Файл с тестами эндпоинтов."""
import io
from decimal import Decimal

import pytest
from fastapi import UploadFile
from fastapi.testclient import TestClient

from src.main import app

test_file_one = UploadFile(io.BytesIO(b'There is nothing here'))
test_file_two = UploadFile(io.BytesIO(b'Here is nothing too'))


@pytest.mark.parametrize('endpoint_url, req', [
    pytest.param('api/balance', 'get', id='balance'),
    pytest.param('api/balance/history', 'get', id='balance_history'),
    pytest.param('api/withdrawal', 'post', id='withdrawal'),
    pytest.param('api/deposit', 'post', id='deposit'),
    pytest.param('api/verify', 'post', id='verify'),
])
def test_four_o_one_response(endpoint_url, req):
    """
    Тест на 401.

    Args:
        endpoint_url (str): URL эндпоинта.
        req (str): Тип запроса.
    """
    client = TestClient(app)
    if req == 'get':
        response = client.get(url=endpoint_url)
    else:
        response = client.post(url=endpoint_url)

    assert response.status_code == 401


@pytest.mark.parametrize('endpoint_url, req, request_params', [
    pytest.param(
        'api/balance',
        'get',
        {'card_number': '8675309'},
        id='balance',
    ),
    pytest.param(
        'api/withdrawal',
        'post',
        {'card_number': '8675309', 'amount': Decimal(100)},
        id='withdrawal',
    ),
    pytest.param(
        'api/deposit',
        'post',
        {'card_number': '8675309', 'amount': Decimal(100)},
        id='deposit',
    ),
])
def test_five_hundred_response(
    endpoint_url,
    req,
    request_params,
    good_client_with_token,
):
    """
    Тест на 500 ответ.

    Args:
        endpoint_url (str): URL эндпоинта.
        req (str): Тип запроса.
        request_params (dict): Параметры запроса.
        good_client_with_token (tuple[TestClient, dict]): Клиент и токен.
    """
    client = good_client_with_token[0]
    token = good_client_with_token[1]
    with pytest.raises(ValueError):
        if req == 'get':
            client.get(
                url=endpoint_url,
                params=request_params,
                headers=token,
            )
        else:
            client.post(
                url=endpoint_url,
                params=request_params,
                headers=token,
            )


@pytest.mark.parametrize('deposit_sum, expected', [
    pytest.param(Decimal(100), True, id='normal sum'),
    pytest.param(Decimal(0), False, id='Zero sum'),
    pytest.param(Decimal(-100), False, id='negative sum'),
    pytest.param(Decimal(1000000000000), True, id='big depo'),
    pytest.param(Decimal(100.998), True, id='decimal'),
])
def test_deposit(deposit_sum, expected, good_client_with_token):
    """
    Тест на депозит.

    Args:
        deposit_sum (Decimal): Сумма депозита.
        expected (bool): Ожидаемый результат.
        good_client_with_token (tuple[TestClient, dict]): Клиент и токен.
    """
    client = good_client_with_token[0]
    token = good_client_with_token[1]
    if not expected:    # noqa: WPS504
        with pytest.raises(ValueError):
            client.post(
                url='api/deposit',
                params={
                    'card_number': '123',
                    'amount': deposit_sum,
                },
                headers=token,
            )
    else:
        response = client.post(
            url='api/deposit',
            params={
                'card_number': '123',
                'amount': deposit_sum,
            },
            headers=token,
        )
        cur_bal = Decimal(response.json()['balance'])

        response = client.post(
            url='api/deposit',
            params={
                'card_number': '123',
                'amount': deposit_sum,
            },
            headers=token,
        )
        expected_balance = cur_bal + deposit_sum

        assert response.status_code == 200
        assert response.json()['card_number'] == '123'
        assert response.json()['balance'] == str(expected_balance)
