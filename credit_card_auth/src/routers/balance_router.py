"""Роутер для получения баланса."""
from datetime import datetime

import httpx
from fastapi import APIRouter, Depends, HTTPException

from config.config import BALANCE_APP_HOST, BALANCE_APP_PORT
from credit_card_auth.src.schemas.log_schemas import BalanceLogModel
from credit_card_auth.src.schemas.user_schemas import UserBalanceRequest
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
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://{BALANCE_APP_HOST}:{BALANCE_APP_PORT}/balance",
            params={
                "card_number": card_number,
            }
        )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()


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
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://{BALANCE_APP_HOST}:{BALANCE_APP_PORT}/balance/history",
            params={
                "card_number": card_number,
                "from_date": from_date,
                "to_date": to_date
            }
        )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()
