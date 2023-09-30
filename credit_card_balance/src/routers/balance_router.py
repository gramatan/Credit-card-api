"""Роутер для получения баланса."""
from datetime import datetime

from fastapi import APIRouter, Depends

from credit_card_balance.src.schemas.log_schemas import BalanceLogModel
from credit_card_balance.src.services.balance_service import BalanceService

router = APIRouter()


@router.get('/balance/history')
async def read_balance_history(
    card_number: str,
    from_date: datetime,
    to_date: datetime,
    response: BalanceService = Depends(),
) -> list[BalanceLogModel]:
    """
    Получение истории баланса.

    Args:
        card_number (str): Номер карты.
        from_date (datetime): Дата начала.
        to_date (datetime): Дата конца.
        response (BalanceService): Сервис для работы с балансом.

    Returns:
        list[BalanceLogModel]: История баланса.
    """
    return await response.get_balance_story(
        card_number,
        from_date,
        to_date,
    )
