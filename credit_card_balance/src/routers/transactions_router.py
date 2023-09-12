"""Роутер для работы с транзакциями."""
from decimal import Decimal

from fastapi import APIRouter

from credit_card_balance.src.database.database import get_db
from credit_card_balance.src.schemas.transactions_schemas import (
    TransactionRequest,
)
from credit_card_balance.src.services.transactions_service import (
    TransactionsService,
)

router = APIRouter()


@router.post('/withdrawal')
async def withdrawal(
    card_number: str,
    amount: Decimal,
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
    return await transactions_service.withdrawal(card_number, amount)


@router.post('/deposit')
async def deposit(
    card_number: str,
    amount: Decimal,
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
    return await transactions_service.deposit(card_number, amount)


@router.post('/verify')
async def verify(
    card_number: str,
    verified: bool,
) -> None:
    """
    Эндпоинт для повышения лимита после верификации.

    Args:
        card_number (str): Номер карты.
        verified (bool): Подтверждение верификации.
    """
    storages = get_db()
    transactions_service = TransactionsService(storages)
    await transactions_service.limit_change(card_number, verified)
