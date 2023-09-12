"""Сервис для роутера верификации пользователя."""
import asyncio

from deepface import DeepFace

from credit_card_verify.src.schemas.verify_schemas import VerificationResponse


class VerifyService:
    """Сервис для верификации пользователя."""

    async def verify(
        self,
        selfie_path: str,
        document_path: str,
    ) -> VerificationResponse:
        """
        Сервис для верификации пользователя.

        Args:
            selfie_path (str): Путь к Селфи пользователя.
            document_path (str): Путь к Документ пользователя.

        Returns:
            VerificationResponse: Результат верификации.
        """
        from main_verify import executor  # noqa: WPS433

        loop = asyncio.get_running_loop()
        verification_result = await loop.run_in_executor(
            executor,
            DeepFace.verify,
            selfie_path,
            document_path,
        )

        return VerificationResponse(verified=verification_result['verified'])
