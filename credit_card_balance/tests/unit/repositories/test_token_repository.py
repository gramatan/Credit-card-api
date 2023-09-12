"""Тесты репозитория токенов."""
from datetime import timedelta

import jwt
import pytest

from config.config import ALGORITHM, SECRET_KEY
from credit_card_balance.src.repositories.token_repository import (
    TokenRepository,
)
from credit_card_balance.tests.unit.conftest import create_token


@pytest.mark.parametrize('test_data, expires_delta', [
    pytest.param(
        ['this_is_not_a_dict'],
        None,
        id='invalid data type list',
    ),
    pytest.param(
        None,
        None,
        id='invalid data type none',
    ),
])
def test_create_access_token_exceptions(test_data, expires_delta):
    """
    Проверка исключений при создании токена.

    Args:
        test_data (any): Данные для токена.
        expires_delta (timedelta): Время жизни токена.
    """
    repo = TokenRepository()
    with pytest.raises((AttributeError, AssertionError)):
        repo.create_access_token(test_data, expires_delta)


@pytest.mark.parametrize('test_data, expires_delta', [
    pytest.param(
        {'sub': 'test_user'},
        timedelta(minutes=1),
        id='normal data with delta',
    ),
    pytest.param(
        {'sub': 'test_user2'},
        None,
        id='normal data without delta',
    ),
    pytest.param(
        {'sub': 'a' * 1000},
        None,
        id='long string',
    ),
])
def test_create_access_token_with_sub(test_data, expires_delta):
    """
    Проверка создания токена.

    Args:
        test_data (dict): Данные для токена.
        expires_delta (timedelta): Время жизни токена.
    """
    repo = TokenRepository()
    token = repo.create_access_token(test_data, expires_delta)
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert 'exp' in decoded_token
    assert decoded_token['sub'] == test_data.get('sub')


@pytest.mark.parametrize('test_data, expires_delta', [
    pytest.param(
        {},
        None,
        id='empty data',
    ),
    pytest.param(
        {f'key{index}': 'value' for index in range(100)},
        None,
        id='many keys',
    ),
])
def test_create_access_token_without_sub(test_data, expires_delta):
    """
    Проверка создания токена.

    Args:
        test_data (dict): Данные для токена.
        expires_delta (timedelta): Время жизни токена.
    """
    repo = TokenRepository()
    token = repo.create_access_token(test_data, expires_delta)
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert 'exp' in decoded_token


@pytest.mark.parametrize('token_type, expected', [
    pytest.param('normal', True, id='normal token'),
    pytest.param('expired', False, id='expired token'),
    pytest.param('wrong_secret_key', False, id='wrong secret key'),
    pytest.param('no_sub_field', False, id='no sub field'),
])
def test_verify_token(token_type, expected, valid_token_data):
    """
    Проверка верификации токена.

    Args:
        token_type (str): Тип токена.
        expected (bool): Ожидаемый результат.
        valid_token_data (dict): Валидные данные для токена.
    """
    repo = TokenRepository()
    token = create_token(valid_token_data, token_type)
    assert repo.verify_token(token) == expected