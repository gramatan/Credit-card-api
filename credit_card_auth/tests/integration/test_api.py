"""Тесты для API."""
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from main_auth import app


@pytest.mark.asyncio
class TestApi:
    """Класс для тестирования API."""

    @pytest_asyncio.fixture(scope='module')
    async def test_client(self):
        """
        Фикстура для создания клиента для тестирования.

        Yields:
            TestClient: Клиент для тестирования.
        """
        yield TestClient(app)

    @pytest.mark.parametrize('endpoint_url, req', [
        pytest.param('api/balance', 'get', id='balance'),
        pytest.param('api/balance/history', 'get', id='balance_history'),
        pytest.param('api/withdrawal', 'post', id='withdrawal'),
        pytest.param('api/deposit', 'post', id='deposit'),
        pytest.param('api/verify', 'post', id='verify'),
    ])
    async def test_four_o_one_response(self, endpoint_url, req, test_client):
        """
        Тест на 401.

        Args:
            endpoint_url (str): URL эндпоинта.
            req (str): Тип запроса.
            test_client (TestClient): Клиент для тестирования.
        """
        client = test_client
        if req == 'get':
            response = client.get(url=endpoint_url)
        else:
            response = client.post(url=endpoint_url)

        assert response.status_code == 401
