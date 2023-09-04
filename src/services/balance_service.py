"""Сервиис для работы с балансом пользователя."""
from src.repositories.transactions import Transactions
from src.schemas.balance_schemas import BalanceResponse


class BalanceService:
    """Сервис для работы с балансом пользователя."""

    def __init__(
        self,
        transactions: Transactions,
    ):
        """
        Инициализация сервиса.

        Args:
            transactions (Transactions): Репо транзакций.
        """
        self.transactions = transactions

    async def get_balance(
        self,
        card_number: str,
    ) -> BalanceResponse:
        """
        Получение баланса.

        Args:
            card_number (str): Номер карты.

        Returns:
            BalanceResponse: Баланс.
        """
        user_balance = self.transactions.get_balance(card_number)
        return BalanceResponse(balance=user_balance)
