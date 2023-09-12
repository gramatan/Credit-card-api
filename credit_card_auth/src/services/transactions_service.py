"""Сервис для транзакций."""
import asyncio
from decimal import Decimal

from deepface import DeepFace
from fastapi import File, UploadFile

from config.config import UNVERIFIED_BALANCE, VERIFIED_BALANCE
from credit_card_auth.src.repositories.log_storage import LogStorage
from credit_card_auth.src.repositories.token_repository import (
    TokenRepository,
)
from credit_card_auth.src.repositories.transactions import Transactions
from credit_card_auth.src.repositories.user_storage import UserStorage
from credit_card_auth.src.schemas.transactions_schemas import (
    TransactionRequest,
    VerificationRequest,
)
from credit_card_auth.src.services.handler_utils import (
    raise_unauthorized_exception,
)


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

    async def verify(   # noqa: WPS210
        self,
        card_number: str,
        token: str,
        selfie: UploadFile = File(...),
        document: UploadFile = File(...),
    ) -> VerificationRequest:
        """
        Сервис для верификации пользователя.

        Args:
            card_number (str): Номер карты.
            token (str): Токен.
            selfie (UploadFile): Селфи пользователя.
            document (UploadFile): Документ пользователя.

        Returns:
            VerificationRequest: Результат верификации.
        """
        if not self.token_repo.verify_token(token):
            raise_unauthorized_exception()

        verification_result = await self._verify(card_number, selfie, document)

        if verification_result:
            new_limit = Decimal(VERIFIED_BALANCE)
            verification_response = VerificationRequest(verified=True)
        else:
            new_limit = Decimal(UNVERIFIED_BALANCE)
            verification_response = VerificationRequest(verified=False)

        self.transactions.change_limit(
            card_number=card_number,
            new_limit=new_limit,
        )

        return verification_response

    async def _verify(self, card_number, selfie, document):  # noqa: WPS210
        from main_balance import executor  # noqa: WPS433

        selfie_path = f'{card_number}_selfie_tmp.jpg'
        document_path = f'{card_number}_document_tmp.jpg'

        with open(selfie_path, 'wb') as selfie_buffer:
            selfie_buffer.write(selfie.file.read())

        with open(document_path, 'wb') as doc_buffer:
            doc_buffer.write(document.file.read())

        loop = asyncio.get_running_loop()
        verification_result = await loop.run_in_executor(
            executor,
            DeepFace.verify,
            selfie_path,
            document_path,
        )
        return verification_result['verified']
