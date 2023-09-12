"""Сервис для транзакций."""
from decimal import Decimal

from credit_card_balance.src.repositories.log_storage import LogStorage
from credit_card_balance.src.repositories.transactions import Transactions
from credit_card_balance.src.repositories.user_storage import UserStorage
from credit_card_balance.src.schemas.transactions_schemas import (
    TransactionRequest,
)


class TransactionsService:
    """Сервиис для работы с транзакциями."""

    def __init__(
        self,
        storages: tuple[Transactions, UserStorage, LogStorage],
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

    async def deposit(
        self,
        card_number: str,
        amount: Decimal,
    ) -> TransactionRequest:
        """
        Сервис для пополнения карты.

        Args:
            card_number (str): Номер карты.
            amount (Decimal): Сумма.

        Returns:
            TransactionRequest: Новый баланс.
        """
        new_balance = self.transactions.deposit(card_number, amount)

        return TransactionRequest(
            card_number=card_number,
            balance=new_balance,
        )

    async def withdrawal(
        self,
        card_number: str,
        amount: Decimal,
    ) -> TransactionRequest:
        """
        Сервис для снятия денег с карты.

        Args:
            card_number (str): Номер карты.
            amount (Decimal): Сумма.

        Returns:
            TransactionRequest: Новый баланс.
        """

        new_balance = self.transactions.withdraw(card_number, amount)

        return TransactionRequest(
            card_number=card_number,
            balance=new_balance,
        )

    async def limit_change(
        self,
        card_number: str,
        verified: bool,
    ):
        """
        Сервис для изменения лимита.

        Args:
            card_number (str): Номер карты.
            verified (bool): Подтверждение верификации.
        """
        if verified:
            new_limit = Decimal(100000)
        else:
            new_limit = Decimal(20000)

        self.transactions.change_limit(card_number, new_limit)
