"""Тесты для репозитория UserStorage."""
from decimal import Decimal

import pytest

from src.models.user import User


@pytest.mark.parametrize('card_number, user_info, expected', [
    pytest.param(
        '1234567890123456',
        {'name': 'John'},
        True,
        id='Add_new_user',
    ),
    pytest.param(
        '1234567890',
        {'name': 'John'},
        'Raises',
        id='User already exist',
    ),
    pytest.param(
        '123456',
        None,
        True,
        id='Empty user info',
    ),
])
def test_add_success(
    card_number,
    user_info,
    expected,
    not_empty_storage,
):
    """
    Тест для проверки добавления пользователя.

    Args:
        card_number (str): Номер карты.
        user_info (dict): Информация о пользователе.
        expected (bool): Ожидаемый результат.
        not_empty_storage (UserStorage): Хранилище с готовым пользователем.
    """
    if expected == 'Raises':
        with pytest.raises(ValueError):
            not_empty_storage.add(card_number, user_info)
    else:
        not_empty_storage.add(card_number, user_info)
        assert expected == (card_number in not_empty_storage._active)


@pytest.mark.parametrize('card_number, expected_type, expected', [
    pytest.param('1234567890123456', type(None), True, id='User exists'),
    pytest.param('1234567890', User, True, id='User not exists'),
])
def test_get_user(card_number, expected_type, expected, not_empty_storage):
    """
    Тест для проверки получения пользователя.

    Args:
        card_number (str): Номер карты.
        expected_type (type): Ожидаемый тип.
        expected (bool): Ожидаемый результат.
        not_empty_storage (UserStorage): Хранилище с готовым пользователем.
    """
    test_result = isinstance(
        not_empty_storage.get_user(card_number),
        expected_type,
    )
    if isinstance(test_result, User):
        assert not_empty_storage.get_user(
            card_number,
        ).card_number == card_number
    assert test_result == expected


@pytest.mark.parametrize('card_number, new_limit, expected_limit, exception', [
    pytest.param(
        '1234567890',
        Decimal(500),
        Decimal(500),
        None,
        id='User exists',
    ),
    pytest.param(
        '9876543210',
        Decimal(500),
        None,
        'Raises',
        id='User not exists',
    ),
])
def test_update_user(
    card_number,
    new_limit,
    expected_limit,
    exception,
    not_empty_storage,
):
    """
    Тест для проверки обновления пользователя.

    Args:
        card_number (str): Номер карты.
        new_limit (Decimal): Новый лимит.
        expected_limit (Decimal): Ожидаемый лимит.
        exception (str): Ожидаемое исключение.
        not_empty_storage (UserStorage): Хранилище с готовым пользователем.
    """
    if exception == 'Raises':
        with pytest.raises(ValueError):
            user = User(
                card_number=card_number,
                limit=Decimal(0),
                info={},
                _balance=Decimal(0),
            )
            not_empty_storage.update_user(user)
    else:
        user = not_empty_storage.get_user(card_number)
        user.limit = new_limit
        updated_user = not_empty_storage.update_user(user)
        assert updated_user.limit == expected_limit
        assert not_empty_storage.get_user(card_number).limit == expected_limit


@pytest.mark.parametrize('card_number, expected', [
    pytest.param('1234567890', True, id='User exists'),
    pytest.param('9876543210', False, id='User not exists'),
])
def test_close(card_number, expected, not_empty_storage):
    """
    Тест для проверки закрытия пользователя.

    Args:
        card_number (str): Номер карты.
        expected (bool): Ожидаемый результат.
        not_empty_storage (UserStorage): Хранилище с готовым пользователем.
    """
    if not expected:    # noqa: WPS504
        with pytest.raises(ValueError):
            not_empty_storage.close(card_number)
    else:
        not_empty_storage.close(card_number)
        assert card_number not in not_empty_storage._active
        in_cloased = [user.card_number for user in not_empty_storage._closed]
        assert card_number in in_cloased
