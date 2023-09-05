"""Роутер для получения баланса."""
from fastapi import APIRouter, Depends

from src.database.database import get_db

from src.schemas.balance_schemas import BalanceResponse
from src.services.balance_service import BalanceService
from src.services.handler_utils import oauth2_scheme

router = APIRouter()


@router.get('/balance/{card_number}', response_model=BalanceResponse)
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
    return await balance_service.get_balance(card_number)
