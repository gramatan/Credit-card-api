"""Репозиторий для работы с пользователем API."""
from fastapi import HTTPException, status

from credit_card_auth.src.database.database import api_user, pwd_context


class ApiUserRepository:
    """Репозиторий для работы с пользователем API."""

    def check_user(self, username: str, password: str) -> bool:
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
        check_user_exist = username == api_user['username']
        check_pass_correct = pwd_context.verify(password, api_user['password'])

        if not (check_user_exist and check_pass_correct):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={'WWW-Authenticate': 'Bearer'},
            )

        return True
