"""Сервис для роутера верификации пользователя."""
import asyncio

from aiohttp import ClientSession, TCPConnector
from deepface import DeepFace

from config.config import BALANCE_APP_PORT, BALANCE_APP_HOST


class VerifyService:
    """Сервис для верификации пользователя."""

    async def verify(
        self,
        card_number: str,
        selfie_path: str,
        document_path: str,
    ) -> bool:
        """
        Сервис для верификации пользователя.

        Args:
            card_number (str): Номер карты.
            selfie_path (str): Путь к Селфи пользователя.
            document_path (str): Путь к Документ пользователя.

        Returns:
            bool: Результат верификации.
        """
        from main_verify import executor  # noqa: WPS433

        loop = asyncio.get_running_loop()
        try:
            verification_result_dict = await loop.run_in_executor(
                executor,
                DeepFace.verify,
                selfie_path,
                document_path,
            )
            verification_result = bool(verification_result_dict['verified'])
        except ValueError:
            verification_result = False

        await self.change_limit(
            card_number=card_number,
            verification_result=verification_result,
        )

        return verification_result

    async def change_limit(
        self,
        card_number: str,
        verification_result: bool,
    ) -> None:
        """
        Изменение лимита пользователя по результатам верификации.

        Args:
            card_number (str): Идентификатор пользователя.
            verification_result (bool): Результат верификации.
        """
        verified_str = str(verification_result).lower()
        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            response = await session.post(
                f'http://{BALANCE_APP_HOST}:{BALANCE_APP_PORT}/api/verify',
                params={
                    "card_number": card_number,
                    "verified": verified_str,
                })
            print(response)
