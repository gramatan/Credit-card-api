"""Репо для работы с транзакциями."""
from fastapi import Depends

from config.config import (
    AMOUNT_ERROR,
    FIRST_USER_FIELD,
    SECOND_USER_FIELD,
    USER_BALANCE_LIMIT_ERROR,
    USER_NOT_FOUND_ERROR,
)
from credit_card_balance.src.database.base import (
    BalanceLogAlchemyModel,
    CommonLogAlchemyModel,
)
from credit_card_balance.src.repositories.log_storage import LogStorage
from credit_card_balance.src.repositories.user_storage import UserStorage


class Transactions:     # noqa: WPS214
    """Класс для работы с транзакциями."""

    def __init__(
        self,
        user_storage: UserStorage = Depends(UserStorage),
        history: LogStorage = Depends(LogStorage),
    ):
        """
        Инициализация репозитория.

        Args:
            user_storage (UserStorage): Репо пользователей.
            history (LogStorage): Репо логов.
        """
        self._user_storage = user_storage
        self._history = history

    async def get_balance(self, card_number: str) -> int:
        """
        Получение баланса.

        Args:
            card_number (str): Номер карты.

        Raises:
            ValueError: Если пользователь не найден.

        Returns:
            int: Баланс в копейках.
        """
        user = await self._user_storage.get_user(card_number)
        if user:
            return user.card_balance
        raise ValueError(USER_NOT_FOUND_ERROR)

    async def withdraw(self, card_number: str, amount: int) -> int:
        """
        Снятие денег.

        Args:
            card_number (str): Номер карты.
            amount (int): Сумма в копейках.

        Raises:
            ValueError: Если неправильная сумма операции.

        Returns:
            int: Баланс в копейках.
        """
        if not self._check_amount(amount):
            raise ValueError(AMOUNT_ERROR)
        return await self._change_balance(card_number, -amount)

    async def deposit(self, card_number: str, amount: int) -> int:
        """
        Пополнение баланса.

        Args:
            card_number: Номер карты.
            amount: Сумма пополнения в копейках.

        Raises:
            ValueError: Если неправильная сумма операции.

        Returns:
            int: Баланс в копейках.
        """
        if not self._check_amount(amount):
            raise ValueError(AMOUNT_ERROR)
        return await self._change_balance(card_number, amount)

    async def update_info(self, card_number: str, user_info: dict) -> None:
        """
        Обновление информации о пользователе.

        Args:
            card_number (str): Номер карты.
            user_info (dict): Информация для обновления.

        Raises:
            ValueError: Если пользователь не найден.
        """
        user = await self._user_storage.get_user(card_number)
        if not user:
            raise ValueError(USER_NOT_FOUND_ERROR)

        if FIRST_USER_FIELD in user_info:
            user.card_first_name = user_info[FIRST_USER_FIELD]

        if SECOND_USER_FIELD in user_info:
            user.card_second_name = user_info[SECOND_USER_FIELD]

        await self._user_storage.update_user(user)

        log = CommonLogAlchemyModel(
            card_number_id=user.id,
            limit_before=user.card_limit,
            limit_after=user.card_limit,
            changes=0,
        )
        await self._history.save(log)

    async def change_limit(self, card_number: str, new_limit: int) -> None:
        """
        Изменение лимита пользователя.

        Args:
            card_number (str): Номер карты.
            new_limit (int): Новый лимит в копейках.

        Raises:
            ValueError: Если пользователь не найден.
        """
        if not self._check_amount(new_limit):
            raise ValueError(AMOUNT_ERROR)

        user = await self._user_storage.get_user(card_number)
        if not user:
            raise ValueError(USER_NOT_FOUND_ERROR)

        old_limit = user.card_limit
        user.card_limit = new_limit
        await self._user_storage.update_user(user)

        log = CommonLogAlchemyModel(
            card_number_id=user.id,
            limit_before=old_limit,
            limit_after=user.card_limit,
            changes=new_limit - old_limit,
        )
        await self._history.save(log)

    async def _change_balance(self, card_number: str, amount: int) -> int:
        """
        Изменение баланса.

        Args:
            card_number: Номер карты.
            amount: Сумма изменения.

        Raises:
            ValueError: Если пользователь не найден.
            ValueError: Если новый баланс меньше лимита.

        Returns:
            int: Новый баланс.
        """
        user = await self._user_storage.get_user(card_number)
        if not user:
            raise ValueError(USER_NOT_FOUND_ERROR)

        new_balance: int = user.card_balance + amount
        if new_balance < -user.card_limit:
            raise ValueError(USER_BALANCE_LIMIT_ERROR)

        old_balance = user.card_balance
        user.card_balance = new_balance

        log = BalanceLogAlchemyModel(
            card_number_id=user.id,
            balance_before=old_balance,
            balance_after=user.card_balance,
            changes=amount,
        )
        await self._history.save(log)

        await self._user_storage.update_user(user)
        return user.card_balance

    def _check_amount(self, amount: int) -> bool:
        """
        Проверка суммы операции. TBD.

        Args:
            amount: сумма операции.

        Returns:
            bool: True, если сумма операции корректна.
        """
        return amount > 0
