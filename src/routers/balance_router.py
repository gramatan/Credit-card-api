"""Роутер для получения баланса."""
from datetime import datetime

from fastapi import APIRouter, Depends

from src.database.database import get_db
from src.schemas.log_schemas import BalanceLogModel
from src.schemas.user_schemas import UserBalanceRequest
from src.services.balance_service import BalanceService
from src.services.handler_utils import oauth2_scheme

router = APIRouter()


@router.get('/balance', response_model=UserBalanceRequest)
async def read_balance(
    card_number: str,
    token: str = Depends(oauth2_scheme),
) -> UserBalanceRequest:
    """
    Получение баланса.

    Args:
        card_number (str): Номер карты.
        token (str): Токен.

    Returns:
        UserBalanceRequest: Баланс.
    """
    storages = get_db()
    balance_service = BalanceService(storages)
    return await balance_service.get_balance(card_number, token)


@router.get('/balance/history', response_model=list[BalanceLogModel])
async def read_balance_history(
    card_number: str,
    from_date: datetime,
    to_date: datetime,
    token: str = Depends(oauth2_scheme),
) -> list[BalanceLogModel]:
    """
    Получение истории баланса.

    Args:
        card_number (str): Номер карты.
        from_date (datetime): Дата начала.
        to_date (datetime): Дата конца.
        token (str): Токен.

    Returns:
        list[BalanceLogModel]: История баланса.
    """
    storages = get_db()
    balance_service = BalanceService(storages)
    return await balance_service.get_balance_story(
        card_number,
        from_date,
        to_date,
        token,
    )
