"""Конфтест для интеграционных тестов."""
import io

import pytest
from fastapi.testclient import TestClient

from main_auth import app


@pytest.fixture()
def good_client():
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


@pytest.fixture()
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
