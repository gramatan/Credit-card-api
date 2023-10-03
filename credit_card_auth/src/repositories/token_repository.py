"""Репозиторий для работы с токенами."""
from datetime import datetime, timedelta

import jwt

from config.config import ALGORITHM, SECRET_KEY, TOKEN_TTL


class TokenRepository:
    """Репозиторий для работы с токенами."""

    async def create_access_token(
        self,
        token_data: dict,
        expires_delta: timedelta | None = None,
    ):
        """
        Создание токена.

        Args:
            token_data (dict): Данные для токена.
            expires_delta (timedelta, optional): Время жизни токена.

        Returns:
            str: Сгенерированный токен.
        """
        to_encode = token_data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=TOKEN_TTL)
        to_encode.update({'exp': expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    async def verify_token(self, token: str):
        """Функция проверки токена.

        Args:
            token (str): Токен.

        Returns:
            bool: Результат проверки.
        """
        try:
            return jwt.decode(
                token.encode(),
                SECRET_KEY,
                algorithms=[ALGORITHM],
            ).get('sub') is not None

        except jwt.PyJWTError:
            return False
