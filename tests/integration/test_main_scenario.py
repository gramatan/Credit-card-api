"""Интеграционный тест с основным сценарием работы приложения."""
from datetime import datetime, timedelta
from decimal import Decimal


def test_open_card(transaction_repo, user_data):
    """
    Тест открытия карты.

    Args:
        transaction_repo (Transactions): Репозиторий транзакций.
        user_data (dict): Данные для тестов.
    """
    card_number = user_data['card_number']
    user_info = user_data['create_user']['info']
    transaction_repo._user_storage.add(card_number, user_info)
    user_balance = transaction_repo.get_balance(card_number)
    assert user_balance == Decimal(0)


def test_increase_limit(transaction_repo, user_data):
    """
    Тест увеличения лимита.

    Args:
        transaction_repo (Transactions): Репозиторий транзакций.
        user_data (dict): Данные для тестов.
    """
    card_number = user_data['card_number']
    new_limit = user_data['increase_limit']['amount']
    transaction_repo.change_limit(card_number, new_limit)
    user = transaction_repo._user_storage.get_user(card_number)
    assert user.limit == new_limit


def test_deposit(transaction_repo, user_data):
    """
    Тест депозита.

    Args:
        transaction_repo (Transactions): Репозиторий транзакций.
        user_data (dict): Данные для тестов.
    """
    card_number = user_data['card_number']
    deposit_amount = user_data['deposit']['amount']
    new_balance = transaction_repo.deposit(card_number, deposit_amount)
    assert new_balance == user_data['deposit']['expected_balance']


def test_withdraw(transaction_repo, user_data):
    """
    Тест снятия.

    Args:
        transaction_repo (Transactions): Репозиторий транзакций.
        user_data (dict): Данные для тестов.
    """
    card_number = user_data['card_number']
    withdraw_amount = user_data['withdraw']['amount']
    new_balance = transaction_repo.withdraw(card_number, withdraw_amount)
    assert new_balance == user_data['withdraw']['expected_balance']


def test_check_balance_log(transaction_repo, user_data):    # noqa: WPS218
    """
    Тест проверки баланса.

    Args:
        transaction_repo (Transactions): Репозиторий транзакций.
        user_data (dict): Данные для тестов.
    """
    card_number = user_data['card_number']
    logs = transaction_repo._history.get_balance_history(
        card_number,
        datetime.utcnow() - timedelta(minutes=1),
        datetime.utcnow() + timedelta(minutes=1),
    )
    assert len(logs) == user_data['get_balance_log']['length']

    for index, log in enumerate(logs):
        expected_log = user_data['get_balance_log']['expected_list'][index]
        assert log.card_number == expected_log.card_number
        assert log.before == expected_log.before
        assert log.after == expected_log.after
        assert log.changes == expected_log.changes

        assert log._datetime_utc.year == expected_log._datetime_utc.year
        assert log._datetime_utc.month == expected_log._datetime_utc.month
        assert log._datetime_utc.day == expected_log._datetime_utc.day
        assert log._datetime_utc.hour == expected_log._datetime_utc.hour
        assert log._datetime_utc.minute == expected_log._datetime_utc.minute
