"""Интеграционный тест сервиса верификации. Мокаем внешние зависимости."""
import asyncio

import pytest

from credit_card_verify.src.services.verify_service import VerifyService


@pytest.fixture(scope='module')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
@pytest.mark.parametrize('verification_result, expected', [
    (True, True),
    (False, False),
])
async def test_verify_service(mocker, verification_result, expected):
    """
    Тест сервиса верификации.

    Args:
        mocker: Фикстура мокера.
        verification_result: Результат верификации.
        expected: Ожидаемый результат.
    """
    mocker.patch(
        'credit_card_verify.src.services.verify_service.VerifyService._get_verification_result',    # noqa: E501
        return_value=verification_result,
    )

    async def mock_response(*args, **kwargs):
        class MockedResponse:
            status_code = 200
            text = 'Mocked response'

            async def json(self):
                return {'response': 'mocked'}

        return MockedResponse()

    mocker.patch('aiohttp.ClientSession.post', new=mock_response)

    verify_service = VerifyService()
    test_result = await verify_service.verify(
        card_number='123',
        selfie_path='path/to/selfie',
        document_path='path/to/document',
    )

    assert test_result == expected
