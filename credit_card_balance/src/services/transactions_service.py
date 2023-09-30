"""Сервис для транзакций."""
from decimal import Decimal

from fastapi import Depends

from config.config import UNVERIFIED_BALANCE, VERIFIED_BALANCE
from credit_card_balance.src.repositories.transactions import Transactions
from credit_card_balance.src.schemas.transactions_schemas import (
    TransactionRequest,
)
from credit_card_balance.src.schemas.user_schemas import UserBalanceRequest
from credit_card_balance.src.services.base_service import BaseService


class TransactionsService(BaseService):
    """Сервиис для работы с транзакциями."""

    def __init__(
        self,
        transactions_repo: Transactions = Depends(Transactions),
    ):
        """
        Инициализация сервиса.

        Args:
            transactions_repo (Transactions): Репо транзакций.
        """
        self.transactions = transactions_repo

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
        user_balance = await self.transactions.get_balance(card_number)
        return UserBalanceRequest(
            card_number=card_number,
            balance=self._kopecks_to_decimal(user_balance),
        )

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
        new_balance = await self.transactions.deposit(
            card_number,
            self._decimal_to_kopecks(amount),
        )

        return TransactionRequest(
            card_number=card_number,
            balance=self._kopecks_to_decimal(new_balance),
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
        new_balance = await self.transactions.withdraw(
            card_number,
            self._decimal_to_kopecks(amount),
        )

        return TransactionRequest(
            card_number=card_number,
            balance=self._kopecks_to_decimal(new_balance),
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
            new_limit = Decimal(VERIFIED_BALANCE)
        else:
            new_limit = Decimal(UNVERIFIED_BALANCE)

        await self.transactions.change_limit(
            card_number,
            self._decimal_to_kopecks(new_limit),
        )
