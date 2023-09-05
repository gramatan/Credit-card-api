"""Сервиис для работы с балансом пользователя."""
from datetime import datetime

from fastapi import Depends

from src.repositories.token_repository import TokenRepository
from src.repositories.transactions import Transactions
from src.schemas.balance_schemas import BalanceResponse
from src.schemas.log_schemas import BalanceLogModel
from src.services.handler_utils import (
    oauth2_scheme,
    raise_unauthorized_exception,
)


class BalanceService:
    """Сервис для работы с балансом пользователя."""

    def __init__(
        self,
        transactions: Transactions,
        token_repository: TokenRepository = TokenRepository(),
    ):
        """
        Инициализация сервиса.

        Args:
            transactions (Transactions): Репо транзакций.
            token_repository (TokenRepository): Репо токенов.
        """
        self.transactions = transactions
        self.token_repo = token_repository

    async def get_balance(
        self,
        card_number: str,
        token: str,
    ) -> BalanceResponse:
        """
        Получение баланса.

        Args:
            card_number (str): Номер карты.
            token (str): Токен.

        Returns:
            BalanceResponse: Баланс.
        """
        if not self.token_repo.verify_token(token):
            raise_unauthorized_exception()
        user_balance = self.transactions.get_balance(card_number)
        return BalanceResponse(balance=user_balance)

    async def get_balance_history(
        self,
        card_number: str,
        from_date: datetime,
        to_date: datetime,
        token: str,
    ) -> list[BalanceLogModel]:
        """
        Получение истории баланса.

        Args:
            card_number (str): Номер карты.
            from_date (datetime): Дата начала.
            to_date (datetime): Дата конца.
            token (str): Токен.

        Returns:
            list[BalanceResponse]: История баланса.
        """
        if not self.token_repo.verify_token(token):
            raise_unauthorized_exception()
        balance_history = self.transactions._history.get_balance_history(
            card_number,
            from_date,
            to_date,
        )
        return [BalanceLogModel(log) for log in balance_history]    # todo: here is an issue
