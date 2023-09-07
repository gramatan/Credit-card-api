"""Файл с тестами эндпоинтов."""
import pytest
from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


@pytest.mark.parametrize('endpoint_url, req', [
    pytest.param('api/balance/123', 'get', id='balance'),
    pytest.param('api/balance/history/123', 'get', id='balance_history'),
    pytest.param('api/withdrawal', 'post', id='withdrawal'),
    pytest.param('api/deposit', 'post', id='deposit'),
    pytest.param('api/verify', 'post', id='verify'),
])
@pytest.mark.asyncio
async def test_401(endpoint_url, req):
    """
    Тест на 401.

    Args:
        endpoint_url (str): URL эндпоинта.
        req (str): Тип запроса.
    """
    if req == 'get':
        response = client.get(url=endpoint_url)
    else:
        response = client.post(url=endpoint_url)

    assert response.status_code == 401
