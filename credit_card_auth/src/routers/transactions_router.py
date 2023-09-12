"""Роутер для работы с транзакциями."""
from decimal import Decimal

from fastapi import APIRouter, Depends, File, UploadFile

from credit_card_auth.src.database.database import get_db
from credit_card_auth.src.schemas.transactions_schemas import (
    TransactionRequest,
    VerificationRequest,
)
from credit_card_auth.src.services.handler_utils import oauth2_scheme
from credit_card_auth.src.services.transactions_service import (
    TransactionsService,
)

router = APIRouter()


@router.post('/withdrawal')
async def withdrawal(
    card_number: str,
    amount: Decimal,
    token: str = Depends(oauth2_scheme),
) -> TransactionRequest:
    """
    Эндпоинт для снятия денег с карты.

    Args:
        card_number (str): Номер карты.
        amount (Decimal): Сумма.
        token (str): Токен.

    Returns:
        TransactionRequest: Новый баланс.
    """
    storages = get_db()
    transactions_service = TransactionsService(storages)
    return await transactions_service.withdrawal(card_number, amount, token)


@router.post('/deposit')
async def deposit(
    card_number: str,
    amount: Decimal,
    token: str = Depends(oauth2_scheme),
) -> TransactionRequest:
    """
    Эндпоинт для пополнения карты.

    Args:
        card_number (str): Номер карты.
        amount (Decimal): Сумма.
        token (str): Токен.

    Returns:
        TransactionRequest: Новый баланс.
    """
    storages = get_db()
    transactions_service = TransactionsService(storages)
    return await transactions_service.deposit(card_number, amount, token)


@router.post('/verify')
async def verify(
    card_number: str,
    selfie: UploadFile = File(...),
    document: UploadFile = File(...),
    token: str = Depends(oauth2_scheme),
) -> VerificationRequest:
    """
    Эндпоинт для верификации пользователя.

    Args:
        card_number (str): Номер карты.
        selfie (UploadFile): Селфи пользователя.
        document (UploadFile): Документ пользователя.
        token (str): Токен.

    Returns:
        VerificationRequest: Результат верификации.
    """
    storages = get_db()
    transactions_service = TransactionsService(storages)
    return await transactions_service.verify(
        card_number,
        token,
        selfie,
        document,
    )
