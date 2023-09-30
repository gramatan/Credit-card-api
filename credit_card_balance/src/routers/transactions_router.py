"""Роутер для работы с транзакциями."""
from decimal import Decimal

from fastapi import APIRouter, Depends

from credit_card_balance.src.schemas.transactions_schemas import (
    TransactionRequest,
)
from credit_card_balance.src.schemas.user_schemas import UserBalanceRequest
from credit_card_balance.src.services.transactions_service import (
    TransactionsService,
)

router = APIRouter()


@router.post('/withdrawal')
async def withdrawal(
    card_number: str,
    amount: Decimal,
    response: TransactionsService = Depends(),
) -> TransactionRequest:
    """
    Эндпоинт для снятия денег с карты.

    Args:
        card_number (str): Номер карты.
        amount (Decimal): Сумма.
        response (TransactionsService): Сервис для работы с транзакциями.

    Returns:
        TransactionRequest: Новый баланс.
    """
    return await response.withdrawal(card_number, amount)


@router.post('/deposit')
async def deposit(
    card_number: str,
    amount: Decimal,
    response: TransactionsService = Depends(),
) -> TransactionRequest:
    """
    Эндпоинт для пополнения карты.

    Args:
        card_number (str): Номер карты.
        amount (Decimal): Сумма.
        response (TransactionsService): Сервис для работы с транзакциями.

    Returns:
        TransactionRequest: Новый баланс.
    """
    return await response.deposit(card_number, amount)


@router.post('/verify')
async def verify(
    card_number: str,
    verified: bool,
    response: TransactionsService = Depends(),
) -> None:
    """
    Эндпоинт для повышения лимита после верификации.

    Args:
        card_number (str): Номер карты.
        verified (bool): Подтверждение верификации.
        response (TransactionsService): Сервис для работы с транзакциями.
    """
    await response.limit_change(card_number, verified)


@router.get('/balance')
async def read_balance(
    card_number: str,
    response: TransactionsService = Depends(),
) -> UserBalanceRequest:
    """
    Получение баланса.

    Args:
        card_number (str): Номер карты.
        response (TransactionsService): Сервис для работы с балансом.

    Returns:
        UserBalanceRequest: Баланс.
    """
    return await response.get_balance(card_number)
