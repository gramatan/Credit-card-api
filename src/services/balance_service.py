"""Сервиис для работы с балансом пользователя."""
from fastapi import Depends

from src.repositories.token_repository import TokenRepository
from src.repositories.transactions import Transactions
from src.schemas.balance_schemas import BalanceResponse
from src.services.handler_utils import oauth2_scheme, raise_unauthorized_exception


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
            raise_unauthorized_exception('Invalid or expired token')
        user_balance = self.transactions.get_balance(card_number)
        return BalanceResponse(balance=user_balance)

    # async def get_balance_story(
    #         self,
    #         card_number: str,
    #         token: str = Depends(oauth2_scheme),
    # ) -> BalanceResponse:
    #     if not self.token_repo.verify_token(token):
    #         raise_unauthorized_exception('Invalid or expired token')
    #     user_balance_story = self.transactions.get_balance_story(card_number)
    #     return user_balance_story