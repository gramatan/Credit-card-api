from decimal import Decimal

from fastapi import File, UploadFile

from src.repositories.token_repository import TokenRepository
from src.repositories.transactions import Transactions
from src.services.handler_utils import raise_unauthorized_exception


class TransactionsService:
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

    async def deposit(
        self,
        card_number: str,
        amount: Decimal,
        token: str,
    ):
        """
        Сервис для пополнения карты.

        Args:
            card_number (str): Номер карты.
            amount (Decimal): Сумма.
            token (str): Токен.
        """
        if not self.token_repo.verify_token(token):
            raise_unauthorized_exception()
        return self.transactions.deposit(card_number, amount)

    async def withdrawal(
        self,
        card_number: str,
        amount: Decimal,
        token: str,
    ):
        """
        Сервис для снятия денег с карты.

        Args:
            card_number (str): Номер карты.
            amount (Decimal): Сумма.
            token (str): Токен.
        """
        if not self.token_repo.verify_token(token):
            raise_unauthorized_exception()
        return self.transactions.withdraw(card_number, amount)

    async def verify(
        self,
        card_number: str,
        token: str,
        selfie: UploadFile = File(...),
        document: UploadFile = File(...),
    ) -> bool:
        """
        Сервис для верификации пользователя.

        Args:
            card_number (str): Номер карты.
            token (str): Токен.
            selfie (UploadFile): Селфи пользователя.
            document (UploadFile): Документ пользователя.

        Returns:
            bool: Результат верификации.
        """
        if not self.token_repo.verify_token(token):
            raise_unauthorized_exception()

        return True
