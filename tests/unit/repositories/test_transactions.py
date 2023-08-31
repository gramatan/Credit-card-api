"""Тесты для репозитория транзакций."""
from decimal import Decimal

import pytest

from tests.unit.conftest import CARD_ID

GOOD_USER = CARD_ID
BAD_USER = '8675309'


@pytest.mark.parametrize('card_id, expected_balance, exception', [
    pytest.param(
        GOOD_USER,
        Decimal('0'),
        None,
        id='User exists',
    ),
    pytest.param(
        BAD_USER,
        None,
        'Raises',
        id='User not exists',
    ),
])
def test_get_balance(
    card_id,
    expected_balance,
    exception,
    transactions_fixture,
):
    """
    Тест метода получения баланса.

    Args:
        card_id (str): Номер карты.
        expected_balance (Decimal): Ожидаемый баланс.
        exception (str): Ожидаемое исключение.
        transactions_fixture (Transactions): Фикстура транзакций.
    """
    if exception == 'Raises':
        with pytest.raises(ValueError):
            transactions_fixture.get_balance(card_id)
    else:
        assert transactions_fixture.get_balance(card_id) == expected_balance


@pytest.mark.parametrize('card_id, amount, expected_balance, exception', [
    pytest.param(
        GOOD_USER,
        Decimal('50'),
        Decimal('-50'),
        None,
        id='Valid',
    ),
    pytest.param(
        GOOD_USER,
        Decimal('0'),
        None,
        'Raises',
        id='Invalid amount',
    ),
    pytest.param(
        BAD_USER,
        Decimal('50'),
        None,
        'Raises',
        id='User not exists',
    ),
    pytest.param(
        GOOD_USER,
        Decimal('5000'),
        None,
        'Raises',
        id='Withdrawal amount > balance',
    ),
])
def test_withdraw(
    card_id,
    amount,
    expected_balance,
    exception,
    transactions_fixture,
):
    """
    Тест метода снятия денег.

    Args:
        card_id (str): Номер карты.
        amount (Decimal): Сумма.
        expected_balance (Decimal): Ожидаемый баланс.
        exception (str): Ожидаемое исключение.
        transactions_fixture (Transactions): Фикстура транзакций.
    """
    if exception == 'Raises':
        with pytest.raises(ValueError):
            transactions_fixture.withdraw(card_id, amount)
    else:
        transactions_fixture.withdraw(card_id, amount)
        assert transactions_fixture.get_balance(card_id) == expected_balance


@pytest.mark.parametrize('card_id, amount, expected_balance, exception', [
    pytest.param(
        GOOD_USER,
        Decimal('50'),
        Decimal('50'),
        None,
        id='Valid',
    ),
    pytest.param(
        GOOD_USER,
        Decimal('0'),
        None,
        'Raises',
        id='Invalid amount',
    ),
    pytest.param(
        BAD_USER,
        Decimal('50'),
        None,
        'Raises',
        id='User not exists',
    ),
])
def test_deposit(
    card_id,
    amount,
    expected_balance,
    exception,
    transactions_fixture,
):
    """
    Тест метода пополнения баланса.

    Args:
        card_id (str): Номер карты.
        amount (Decimal): Сумма.
        expected_balance (Decimal): Ожидаемый баланс.
        exception (str): Ожидаемое исключение.
        transactions_fixture (Transactions): Фикстура транзакций.
    """
    if exception == 'Raises':
        with pytest.raises(ValueError):
            transactions_fixture.deposit(card_id, amount)
    else:
        transactions_fixture.deposit(card_id, amount)
        assert transactions_fixture.get_balance(card_id) == expected_balance


@pytest.mark.parametrize('card_id, new_limit, expected_limit, exception', [
    pytest.param(
        GOOD_USER,
        Decimal('2000'),
        Decimal('2000'),
        None,
        id='Valid',
    ),
    pytest.param(
        GOOD_USER,
        Decimal('-1'),
        None,
        'Raises',
        id='Invalid amount',
    ),
    pytest.param(
        BAD_USER,
        Decimal('2000'),
        None,
        'Raises',
        id='User not exists',
    ),
])
def test_change_limit(  # noqa: WPS211
    card_id,
    new_limit,
    expected_limit,
    exception,
    transactions_fixture,
    not_empty_storage,
):
    """
    Тест метода изменения лимита.

    Args:
        card_id (str): Номер карты.
        new_limit (Decimal): Новый лимит.
        expected_limit (Decimal): Ожидаемый лимит.
        exception (str): Ожидаемое исключение.
        transactions_fixture (Transactions): Фикстура транзакций.
        not_empty_storage (Storage): Хранилище с пользователями.
    """
    if exception == 'Raises':
        with pytest.raises(ValueError):
            transactions_fixture.change_limit(card_id, new_limit)
    else:
        transactions_fixture.change_limit(card_id, new_limit)
        user = not_empty_storage.get_user(card_id)
        assert user.limit == expected_limit


@pytest.mark.parametrize('card_id, new_info, expected_info, exception', [
    pytest.param(
        GOOD_USER,
        {'age': 30},
        {'name': 'John', 'age': 30},
        None,
        id='Add new field to info',
    ),
    pytest.param(
        GOOD_USER,
        {'name': 'Not a John', 'age': 30},
        {'name': 'Not a John', 'age': 30},
        None,
        id='Update existed info and add new',
    ),
    pytest.param(
        GOOD_USER,
        {'name': 'Not a John'},
        {'name': 'Not a John'},
        None,
        id='Update existed info only',
    ),
    pytest.param(
        BAD_USER,
        {'name': 'Not a John'},
        None,
        'Raises',
        id='User not exists',
    ),
])
def test_update_info(
    card_id,
    new_info,
    expected_info,
    exception,
    transactions_fixture,
):
    """
    Тест метода обновления информации о пользователе.

    Args:
        card_id (str): Номер карты.
        new_info (dict): Новая информация.
        expected_info (dict): Ожидаемая информация.
        exception (str): Ожидаемое исключение.
        transactions_fixture (Transactions): Фикстура транзакций.
    """
    storage = transactions_fixture._user_storage

    if exception == 'Raises':
        with pytest.raises(ValueError):
            transactions_fixture.update_info(card_id, new_info)
        return

    transactions_fixture.update_info(card_id, new_info)

    user = storage.get_user(card_id)
    for key, expected_value in expected_info.items():
        assert user.info[key] == expected_value
