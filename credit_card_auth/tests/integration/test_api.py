"""Тесты для API."""
from datetime import datetime
from decimal import Decimal

import httpx
import pytest
from fastapi.testclient import TestClient

from main_auth import app


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


def test_bad_user():
    """Тест на неправильного пользователя."""
    client = TestClient(app)
    response = client.post(
        url='api/auth',
        data={
            'username': 'bad_user',
            'password': 'bad_password',
        },
    )
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
    pytest.param(
        'api/balance/history',
        'get',
        {
            'card_number': '8675309',
            'from_date': datetime(2007, 9, 13),
            'to_date': datetime(2023, 9, 13),
        },
        id='balance_history',
    ),
    pytest.param(
        'api/verify',
        'post',
        {'card_number': '8675309'},
        id='verify',
    ),
])
def test_five_hundred_response(
    endpoint_url,
    req,
    request_params,
    good_client,
    mocker,
    prepare_files,
):
    """
    Тест на получение плохих ответов от других сервисов.

    Args:
        endpoint_url (str): URL эндпоинта.
        req (str): Тип запроса.
        request_params (dict): Параметры запроса.
        good_client (tuple[TestClient, dict]): Клиент и токен.
        mocker: Мокер.
        prepare_files: Подготовленные файлы.
    """
    async def mock_response(*args, **kwargs):
        class MockedResponse:
            status_code = 500
            text = 'It doesnt matter what is here'

            async def json(self):
                return {'error': 'It doesnt matter what is here'}

        return MockedResponse()

    mocker.patch.object(httpx.AsyncClient, 'get', new=mock_response)
    mocker.patch.object(httpx.AsyncClient, 'post', new=mock_response)

    client, token = good_client
    if req == 'get':
        response = client.get(
            url=endpoint_url,
            params=request_params,
            headers=token,
        )

    elif endpoint_url == 'api/verify':
        response = client.post(
            url=endpoint_url,
            params=request_params,
            headers=token,
            files={
                'selfie': prepare_files[0],
                'document': prepare_files[1],
            },
        )

    else:
        response = client.post(
            url=endpoint_url,
            params=request_params,
            headers=token,
        )

    assert response.status_code == 500
