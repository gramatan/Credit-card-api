"""Репозиторий для работы с пользователем API."""
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.postgres_adaptor import get_db_session
from credit_card_auth.src.database.base import UserAlchemyModel
from credit_card_auth.src.database.database import pwd_context


class ApiUserRepository:
    """Репозиторий для работы с пользователем API."""

    def __init__(
        self,
        session: AsyncSession = Depends(get_db_session),
    ):
        """
        Инициализация репозитория.

        Args:
            session (AsyncSession): Сессия для работы с БД.
        """
        self._session = session

    async def check_user(
        self,
        username: str,
        password: str,
    ) -> bool:
        """
        Проверка пользователя.

        Args:
            username (str): Имя пользователя.
            password (str): Пароль.

        Raises:
            HTTPException: Если пользователь не найден или пароль неверный.

        Returns:
            bool: True, если пользователь существует.
        """
        db_request = await self._session.execute(
            select(UserAlchemyModel).filter_by(login=username),
        )
        user = db_request.scalar()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={'WWW-Authenticate': 'Bearer'},
            )

        if not pwd_context.verify(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={'WWW-Authenticate': 'Bearer'},
            )

        return True
