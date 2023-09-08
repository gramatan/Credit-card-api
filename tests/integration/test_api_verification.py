"""Тесты для проверки эндпоинта верификации картинок."""

from decimal import Decimal

import pytest


@pytest.mark.parametrize('verification_result', [
    pytest.param(True, id='True'),
    pytest.param(False, id='False'),
])
def test_verify(
    verification_result,
    prepare_files,
    good_client_with_token,
    mocker,
):
    """
    Тест верификации.

    Args:
        verification_result: Результат верификации.
        prepare_files: Подготовленные файлы.
        good_client_with_token: Клиент и токен.
        mocker: Мокер.
    """
    client, token = good_client_with_token
    file1, file2 = prepare_files

    mocker.patch(
        'src.services.transactions_service.TransactionsService._verify',
        return_value=verification_result,
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
        headers=token,
    )

    if verification_result:
        response = client.post(
            url='api/withdrawal',
            params={
                'card_number': '123',
                'amount': Decimal(100000),
            },
            headers=token,
        )
        assert response.status_code == 200
    else:
        with pytest.raises(ValueError):
            client.post(
                url='api/withdrawal',
                params={
                    'card_number': '123',
                    'amount': Decimal(100000),
                },
                headers=token,
            )
