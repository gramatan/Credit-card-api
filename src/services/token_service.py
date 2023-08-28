"""Сервис для работы с токенами."""
from datetime import timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from config.config import TOKEN_TTL
from src.repositories.token import TokenRepository
from src.schemas.token_schemas import TokenData


class TokenService:
    """Сервис для работы с токенами."""

    def __init__(
        self,
        token_repository: TokenRepository = Depends(),
    ):
        """
        Инициализация сервиса.

        Args:
            token_repository (TokenRepository): Репо токенов.
        """
        self.token_repo = token_repository

    def get_token(
        self,
        form_data: OAuth2PasswordRequestForm = Depends(),
    ) -> TokenData:
        """
        Получение токена.

        Args:
            form_data (OAuth2PasswordRequestForm): Данные формы.

        Returns:
            TokenData: Токен.
        """
        access_token_expires = timedelta(minutes=TOKEN_TTL)
        access_token = self.token_repo.create_access_token(
            token_data={'sub': form_data.username},
            expires_delta=access_token_expires,
        )

        return TokenData(   # noqa: S106
            access_token=access_token,
            token_type='bearer',
        )
