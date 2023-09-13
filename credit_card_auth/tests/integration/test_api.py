"""Тесты для API."""
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
