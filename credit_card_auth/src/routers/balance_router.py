"""Роутер для получения баланса."""
from datetime import datetime

from fastapi import APIRouter, Depends

from credit_card_auth.src.database.database import get_db
from credit_card_auth.src.schemas.log_schemas import BalanceLogModel
from credit_card_auth.src.schemas.user_schemas import UserBalanceRequest
from credit_card_auth.src.services.balance_service import BalanceService
from credit_card_auth.src.services.handler_utils import oauth2_scheme

router = APIRouter()


@router.get('/balance')
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
    return await balance_service.get_balance(card_number)


@router.get('/balance/history')
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
