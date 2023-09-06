"""Репо для работы с транзакциями."""
from datetime import datetime
from decimal import Decimal

from config.config import (
    AMOUNT_ERROR,
    USER_BALANCE_LIMIT_ERROR,
    USER_NOT_FOUND_ERROR,
)
from src.models.logs import BalanceLog, CommonLog
from src.repositories.log_storage import LogStorage
from src.repositories.user_storage import UserStorage


class Transactions:     # noqa: WPS214
    """Класс для работы с транзакциями."""

    def __init__(self, user_storage: UserStorage, history: LogStorage):
        """
        Инициализация репозитория.

        Args:
            user_storage (UserStorage): Репо пользователей.
            history (LogStorage): Репо логов.
        """
        self._user_storage = user_storage
        self._history = history

    def get_balance(self, card_number: str) -> Decimal:
        """
        Получение баланса.

        Args:
            card_number (str): Номер карты.

        Raises:
            ValueError: Если пользователь не найден.

        Returns:
            Decimal: Баланс.
        """
        user = self._user_storage.get_user(card_number)
        if user:
            return user.balance
        raise ValueError(USER_NOT_FOUND_ERROR)

    def withdraw(self, card_number: str, amount: Decimal) -> Decimal:
        """
        Снятие денег.

        Args:
            card_number (str): Номер карты.
            amount (Decimal): Сумма.

        Raises:
            ValueError: Если неправильная сумма операции.

        Returns:
            Decimal: Баланс.
        """
        if not self._check_amount(amount):
            raise ValueError(AMOUNT_ERROR)
        return self._change_balance(card_number, -amount)

    def deposit(self, card_number: str, amount: Decimal) -> Decimal:
        """
        Пополнение баланса.

        Args:
            card_number: Номер карты.
            amount: Сумма пополнения.

        Raises:
            ValueError: Если неправильная сумма операции.

        Returns:
            Decimal: Баланс.
        """
        if not self._check_amount(amount):
            raise ValueError(AMOUNT_ERROR)
        return self._change_balance(card_number, amount)

    def update_info(self, card_number: str, user_info: dict) -> None:
        """
        Обновление информации о пользователе.

        Args:
            card_number (str): Номер карты.
            user_info (dict): Информация для обновления.

        Raises:
            ValueError: Если пользователь не найден.
        """
        user = self._user_storage.get_user(card_number)
        if not user:
            raise ValueError(USER_NOT_FOUND_ERROR)

        user.info.update(user_info)

        self._user_storage.update_user(user)

        log = CommonLog(
            card_number=card_number,
            before=user.limit,
            after=user.limit,
            changes=Decimal(0),
        )
        self._history.save(log)

    def change_limit(self, card_number: str, new_limit: Decimal) -> None:
        """
        Изменение лимита пользователя.

        Args:
            card_number (str): Номер карты.
            new_limit (Decimal): Новый лимит.

        Raises:
            ValueError: Если пользователь не найден.
        """
        if not self._check_amount(new_limit):
            raise ValueError(AMOUNT_ERROR)

        user = self._user_storage.get_user(card_number)
        if not user:
            raise ValueError(USER_NOT_FOUND_ERROR)

        old_limit = user.limit
        user.limit = new_limit
        self._user_storage.update_user(user)

        log = CommonLog(
            card_number=card_number,
            before=old_limit,
            after=new_limit,
            changes=new_limit - old_limit,
        )
        self._history.save(log)

    def _change_balance(self, card_number: str, amount: Decimal) -> Decimal:
        """
        Изменение баланса.

        Args:
            card_number: Номер карты.
            amount: Сумма изменения.

        Raises:
            ValueError: Если пользователь не найден.
            ValueError: Если новый баланс меньше лимита.

        Returns:
            Decimal: Новый баланс.
        """
        user = self._user_storage.get_user(card_number)
        if not user:
            raise ValueError(USER_NOT_FOUND_ERROR)

        new_balance = user.balance + amount

        if new_balance < -user.limit:
            raise ValueError(USER_BALANCE_LIMIT_ERROR)

        old_balance = user.balance
        user.balance = new_balance

        self._history.save(BalanceLog(
            card_number=card_number,
            before=old_balance,
            after=user.balance,
            changes=amount,
            _datetime_utc=datetime.utcnow()
        ))

        self._user_storage.update_user(user)
        return user.balance

    def _check_amount(self, amount: Decimal) -> bool:
        """
        Проверка суммы операции. TBD.

        Args:
            amount: сумма операции.

        Returns:
            bool: True, если сумма операции корректна.
        """
        return amount > 0
