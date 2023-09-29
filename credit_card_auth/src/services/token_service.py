"""Сервис для работы с токенами."""
from datetime import timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from config.config import TOKEN_TTL
from credit_card_auth.src.repositories.api_user_repository import (
    ApiUserRepository,
)
from credit_card_auth.src.repositories.token_repository import TokenRepository
from credit_card_auth.src.schemas.token_schemas import TokenData


class TokenService:
    """Сервис для работы с токенами."""

    def __init__(
        self,
        token_repository: TokenRepository = Depends(),
        api_user_repo: ApiUserRepository = Depends(ApiUserRepository),
    ):
        """
        Инициализация сервиса.

        Args:
            token_repository (TokenRepository): Репо токенов.
            api_user_repo (ApiUserRepository): Репо пользователей API.
        """
        self.token_repo = token_repository
        self.api_user_repo = api_user_repo

    async def get_token(
        self,
        form_data: OAuth2PasswordRequestForm,
    ) -> TokenData:
        """
        Получение токена.

        Args:
            form_data (OAuth2PasswordRequestForm): Данные формы.

        Returns:
            TokenData: Токен.
        """
        await self.api_user_repo.check_user(
            form_data.username,
            form_data.password,
        )
        access_token_expires = timedelta(minutes=TOKEN_TTL)
        access_token = self.token_repo.create_access_token(
            token_data={'sub': form_data.username},
            expires_delta=access_token_expires,
        )

        return TokenData(   # noqa: S106
            access_token=access_token,
            token_type='bearer',
        )
