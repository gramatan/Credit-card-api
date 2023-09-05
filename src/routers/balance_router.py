"""Роутер для получения баланса."""
from datetime import datetime

from fastapi import APIRouter, Depends

from src.database.database import get_db
from src.schemas.balance_schemas import BalanceResponse
from src.services.balance_service import BalanceService
from src.services.handler_utils import oauth2_scheme

router = APIRouter()


@router.get('/balance', response_model=BalanceResponse)
async def read_balance(
    card_number: str,
    token: str = Depends(oauth2_scheme),
) -> BalanceResponse:
    """
    Получение баланса.

    Args:
        card_number (str): Номер карты.
        token (str): Токен.

    Returns:
        BalanceResponse: Баланс.
    """
    transactions = get_db()
    balance_service = BalanceService(transactions)
    return await balance_service.get_balance(card_number, token)


@router.get('/balance/history', response_model=list[BalanceResponse])
async def read_balance_history(
    card_number: str,
    from_date: datetime,
    to_date: datetime,
    token: str = Depends(oauth2_scheme),
) -> list[BalanceResponse]:
    """
    Получение истории баланса.

    Args:
        card_number (str): Номер карты.
        from_date (datetime): Дата начала.
        to_date (datetime): Дата конца.
        token (str): Токен.

    Returns:
        list[BalanceResponse]: История баланса.
    """
    transactions = get_db()
    balance_service = BalanceService(transactions)
    return await balance_service.get_balance_history(
        card_number,
        from_date,
        to_date,
        token,
    )
