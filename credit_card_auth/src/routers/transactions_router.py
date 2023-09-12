"""Роутер для работы с транзакциями."""
from decimal import Decimal

import httpx
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException

from config.config import BALANCE_APP_HOST, BALANCE_APP_PORT, VERIFICATION_APP_HOST, VERIFICATION_APP_PORT
from credit_card_auth.src.schemas.transactions_schemas import (
    TransactionRequest,
    VerificationRequest,
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

    Returns:
        TransactionRequest: Новый баланс.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://{BALANCE_APP_HOST}:{BALANCE_APP_PORT}/api/withdrawal",
            params={
                "card_number": card_number,
                "amount": amount,
            }
        )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

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

    Returns:
        TransactionRequest: Новый баланс.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://{BALANCE_APP_HOST}:{BALANCE_APP_PORT}/api/deposit",
            params={
                "card_number": card_number,
                "amount": amount,
            }
        )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()



@router.post('/verify')
async def verify(
    card_number: str,
    selfie: UploadFile = File(...),
    document: UploadFile = File(...),
    token: str = Depends(oauth2_scheme),
) -> VerificationRequest:
    """
    Эндпоинт для верификации пользователя.

    Args:
        card_number (str): Номер карты.
        selfie (UploadFile): Селфи пользователя.
        document (UploadFile): Документ пользователя.
        token (str): Токен.

    Returns:
        VerificationRequest: Результат верификации.
    """

    # todo: Нам надо сохранить файлы в хранилище
    selfie_path = f'{card_number}_selfie_tmp.jpg'
    document_path = f'{card_number}_document_tmp.jpg'

    with open(selfie_path, 'wb') as selfie_buffer:
        selfie_buffer.write(selfie.file.read())

    with open(document_path, 'wb') as doc_buffer:
        doc_buffer.write(document.file.read())

    # todo: А тут у нас будет кафка
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://{VERIFICATION_APP_HOST}:{VERIFICATION_APP_PORT}/api/verify",
            params={
                "card_number": card_number,
                "selfie": selfie_path,
                "document": document_path,
            }
        )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()