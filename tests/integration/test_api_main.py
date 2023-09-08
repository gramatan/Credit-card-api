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
