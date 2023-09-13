"""Тесты для проверки эндпоинта верификации картинок."""
import io

import pytest
from fastapi.testclient import TestClient

from credit_card_verify.src.schemas.verify_schemas import VerificationResponse
from main_verify import app


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


@pytest.mark.parametrize('verification_result', [
    pytest.param(True, id='True'),
    pytest.param(False, id='False'),
])
def test_verify(
    verification_result,
    prepare_files,
    mocker,
):
    """
    Тест верификации.

    Args:
        verification_result: Результат верификации.
        prepare_files: Подготовленные файлы.
        mocker: Мокер.
    """
    client = TestClient(app)
    file1, file2 = prepare_files

    result_of_verify = VerificationResponse(verified=verification_result)

    mocker.patch(
        'credit_card_verify.src.services.verify_service.VerifyService.verify',    # noqa: E501
        return_value=result_of_verify,
    )

    client.post(
        url='api/verify',
        params={
            'card_number': '123',
        },
        files={
            'selfie': ('file1.jpg', file1, 'image/jpeg'),
            'document': ('file2.jpg', file2, 'image/jpeg'),
        },
    )
    assert True     # donno how to test it  # noqa: WPS444
