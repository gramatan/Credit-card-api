"""Роутер для верификации пользователя."""
from fastapi import APIRouter, Depends, File, Request, UploadFile

from credit_card_auth.src.schemas.transactions_schemas import (
    VerificationRequest,
)
from credit_card_auth.src.services.handler_utils import oauth2_scheme
from credit_card_auth.src.services.verification_service import (
    VerificationService,
)

router = APIRouter()


@router.post('/verify')
async def verify(   # noqa: WPS210
    card_number: str,
    request: Request,
    selfie: UploadFile = File(...),
    document: UploadFile = File(...),
    token: str = Depends(oauth2_scheme),
) -> VerificationRequest:
    """
    Эндпоинт для верификации пользователя.

    Args:
        card_number (str): Номер карты.
        request (Request): Сам запрос для состояний.
        selfie (UploadFile): Селфи пользователя.
        document (UploadFile): Документ пользователя.
        token (str): Токен.

    Returns:
        VerificationRequest: Результат верификации.
    """
    verification_service = VerificationService()
    return await verification_service.verify(
        card_number,
        request,
        selfie,
        document,
    )
