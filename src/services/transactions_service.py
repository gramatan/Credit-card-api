"""Сервис для транзакций."""
from decimal import Decimal

from src.repositories.log_storage import LogStorage
from src.repositories.token_repository import TokenRepository
from src.repositories.transactions import Transactions
from src.repositories.user_storage import UserStorage
from src.schemas.transactions_schemas import TransactionRequest
from src.services.handler_utils import raise_unauthorized_exception


class TransactionsService:
    """Сервиис для работы с транзакциями."""

    def __init__(
        self,
        storages: tuple[Transactions, UserStorage, LogStorage],
        token_repository: TokenRepository = TokenRepository(),
    ):
        """
        Инициализация сервиса.

        Args:
            storages (Transactions, UserStorage, LogStorage): Репо и хранилища.
            token_repository (TokenRepository): Репо токенов.
        """
        self.transactions = storages[0]
        self.user_storage = storages[1]
        self.history = storages[2]
        self.token_repo = token_repository

    async def deposit(
        self,
        card_number: str,
        amount: Decimal,
        token: str,
    ) -> TransactionRequest:
        """
        Сервис для пополнения карты.

        Args:
            card_number (str): Номер карты.
            amount (Decimal): Сумма.
            token (str): Токен.

        Returns:
            TransactionRequest: Новый баланс.
        """
        if not self.token_repo.verify_token(token):
            raise_unauthorized_exception()
        new_balance = self.transactions.deposit(card_number, amount)

        return TransactionRequest(
            card_number=card_number,
            balance=new_balance,
        )

    async def withdrawal(
        self,
        card_number: str,
        amount: Decimal,
        token: str,
    ) -> TransactionRequest:
        """
        Сервис для снятия денег с карты.

        Args:
            card_number (str): Номер карты.
            amount (Decimal): Сумма.
            token (str): Токен.

        Returns:
            TransactionRequest: Новый баланс.
        """
        if not self.token_repo.verify_token(token):
            raise_unauthorized_exception()
        new_balance = self.transactions.withdraw(card_number, amount)

        return TransactionRequest(
            card_number=card_number,
            balance=new_balance,
        )
