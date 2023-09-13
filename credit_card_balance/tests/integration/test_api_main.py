"""Файл с тестами эндпоинтов."""
import io
from decimal import Decimal

import pytest
from fastapi import UploadFile
from fastapi.testclient import TestClient

from main_balance import app

test_file_one = UploadFile(io.BytesIO(b'There is nothing here'))
test_file_two = UploadFile(io.BytesIO(b'Here is nothing too'))


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
):
    """
    Тест на 500 ответ.

    Args:
        endpoint_url (str): URL эндпоинта.
        req (str): Тип запроса.
        request_params (dict): Параметры запроса.
    """
    client = TestClient(app)
    with pytest.raises(ValueError):
        if req == 'get':
            client.get(
                url=endpoint_url,
                params=request_params,
            )
        else:
            client.post(
                url=endpoint_url,
                params=request_params,
            )
