"""Роутер для верификации пользователя."""
from fastapi import APIRouter

from credit_card_verify.src.schemas.verify_schemas import VerificationResponse
from credit_card_verify.src.services.verify_service import VerifyService

router = APIRouter()


@router.post('/verify')
async def verify(
    selfie: str,
    document: str,
) -> VerificationResponse:
    """
    Эндпоинт для верификации пользователя.

    Args:
        selfie (str): путь к Селфи пользователя.
        document (str): путь к Документ пользователя.

    Returns:
        VerificationResponse: Результат верификации.
    """
    verification_service = VerifyService()
    return await verification_service.verify(
        selfie,
        document,
    )
