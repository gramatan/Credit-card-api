from decimal import Decimal

from deepface import DeepFace
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

        selfie_path = "selfie_tmp.jpg"
        document_path = "document_tmp.jpg"
    
        with open(selfie_path, "wb") as buffer:
            buffer.write(selfie.file.read())

        with open(document_path, "wb") as buffer:
            buffer.write(document.file.read())

        result = DeepFace.verify(img1_path=selfie_path, img2_path=document_path)

        new_limit = 20000

        if result['verified'] == True:
            new_limit = 100000

        self.transactions.change_limit(card_number=card_number, new_limit=new_limit)

        return result["verified"]
    