"""Роутер для работы с транзакциями."""
from decimal import Decimal

import httpx
from fastapi import APIRouter, Depends, HTTPException, status

from config.config import BALANCE_APP_HOST, BALANCE_APP_PORT
from credit_card_auth.src.schemas.transactions_schemas import (
    TransactionRequest,
)
from credit_card_auth.src.services.handler_utils import oauth2_scheme

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

    Raises:
        HTTPException: Если не получили ответ 200.

    Returns:
        TransactionRequest: Новый баланс.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f'http://{BALANCE_APP_HOST}:{BALANCE_APP_PORT}/api/withdrawal',
            params={
                'card_number': card_number,
                'amount': amount,   # type: ignore
            },
        )

    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text,
        )

    return response.json()


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

    Raises:
        HTTPException: Если не получили ответ 200.

    Returns:
        TransactionRequest: Новый баланс.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f'http://{BALANCE_APP_HOST}:{BALANCE_APP_PORT}/api/deposit',
            params={
                'card_number': card_number,
                'amount': amount,   # type: ignore
            },
        )

    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text,
        )

    return response.json()
