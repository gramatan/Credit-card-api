"""Тесты эндпоинта верификации."""
import pytest
from fastapi.testclient import TestClient

from main_auth import app


@pytest.mark.parametrize('verification_result', [
    pytest.param(True, id='True'),
    pytest.param(False, id='False'),
])
def test_verify_endpoint(verification_result, prepare_files, mocker):
    """
    Тест верификации эндпоинта.

    Args:
        verification_result: Результат верификации.
        prepare_files: Подготовленные файлы.
        mocker: Мокер.
    """
    client = TestClient(app)
    file1, file2 = prepare_files

    mocker.patch(
        'credit_card_auth.src.services.verification_service.VerificationService._send_message_to_kafka',    # noqa: E501
        return_value=None,
    )
    mocker.patch(
        'credit_card_auth.src.services.verification_service.VerificationService._await_response',           # noqa: E501
        return_value=verification_result,
    )

    response = client.post(
        url='api/verify',
        headers={'Authorization': 'Bearer SOME_TOKEN'},
        params={
            'card_number': '123',
        },
        files={
            'selfie': ('file1.jpg', file1, 'image/jpeg'),
            'document': ('file2.jpg', file2, 'image/jpeg'),
        },
    )

    assert response.status_code == 200
    assert response.json() == {'verified': verification_result}
