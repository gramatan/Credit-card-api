"""Роутер для работы с транзакциями."""
from decimal import Decimal

from fastapi import APIRouter, Depends

from src.database.database import get_db
from src.schemas.transactions_schemas import TransactionRequest
from src.services.handler_utils import oauth2_scheme
from src.services.transactions_service import TransactionsService

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
