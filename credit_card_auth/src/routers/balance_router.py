"""Роутер для получения баланса."""
from datetime import datetime

import httpx
from fastapi import APIRouter, Depends, HTTPException, status

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

    Raises:
        HTTPException: Если не удалось получить баланс.

    Returns:
        UserBalanceRequest: Баланс.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'http://{BALANCE_APP_HOST}:{BALANCE_APP_PORT}/api/balance',
            params={
                'card_number': card_number,
            },
        )

    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text,
        )

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

    Raises:
        HTTPException: Если не удалось получить историю баланса.

    Returns:
        list[BalanceLogModel]: История баланса.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f'http://{BALANCE_APP_HOST}:{BALANCE_APP_PORT}/api/balance/history',    # noqa: E501
            params={
                'card_number': card_number,
                'from_date': from_date,   # type: ignore
                'to_date': to_date,       # type: ignore
            },
        )

    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text,
        )

    return response.json()
