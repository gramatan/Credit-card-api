"""Сервиис для работы с балансом пользователя."""
from datetime import datetime

from credit_card_balance.src.repositories.log_storage import LogStorage
from credit_card_balance.src.repositories.transactions import Transactions
from credit_card_balance.src.repositories.user_storage import UserStorage
from credit_card_balance.src.schemas.log_schemas import BalanceLogModel
from credit_card_balance.src.schemas.user_schemas import UserBalanceRequest


class BalanceService:
    """Сервис для работы с балансом пользователя."""

    def __init__(
        self,
        storages: tuple[Transactions, UserStorage, LogStorage],
    ):
        """
        Инициализация сервиса.

        Args:
            storages (Transactions, UserStorage, LogStorage): Репо и хранилища.
        """
        self.transactions = storages[0]
        self.user_storage = storages[1]
        self.history = storages[2]

    async def get_balance(
        self,
        card_number: str,
    ) -> UserBalanceRequest:
        """
        Получение баланса.

        Args:
            card_number (str): Номер карты.

        Returns:
            UserBalanceRequest: Баланс.
        """
        user_balance = self.transactions.get_balance(card_number)
        return UserBalanceRequest(
            card_number=card_number,
            balance=user_balance,
        )

    async def get_balance_story(
        self,
        card_number: str,
        from_date: datetime,
        to_date: datetime,
    ) -> list[BalanceLogModel]:
        """
        Получение истории баланса.

        Args:
            card_number (str): Номер карты.
            from_date (datetime): Дата начала.
            to_date (datetime): Дата конца.

        Returns:
            list[UserBalanceRequest]: История баланса.
        """
        balance_history = self.history.get_balance_history(
            card_number,
            from_date,
            to_date,
        )
        response: list[BalanceLogModel] = []

        if not balance_history:
            return response

        for log in balance_history:
            response.append(BalanceLogModel(
                card_number=log.card_number,
                before=log.before,
                after=log.after,
                changes=log.changes,
                datetime_utc=log.datetime_utc,
            ))

        return response
