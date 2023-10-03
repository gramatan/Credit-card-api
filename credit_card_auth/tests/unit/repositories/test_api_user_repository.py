"""Тесты для репозитория пользователей."""
import pytest
import pytest_asyncio
from fastapi import HTTPException
from sqlalchemy import delete, insert

from credit_card_auth.src.database.base import UserAlchemyModel, pwd_context
from credit_card_auth.src.repositories.api_user_repository import (
    ApiUserRepository,
)


@pytest.mark.asyncio
class TestUserRepository:
    """Класс для тестирования репозитория пользователей."""

    @pytest_asyncio.fixture
    async def repository(self, db_session):
        """
        Фикстура для создания репозитория пользователей.

        Args:
            db_session: фикстура для создания сессии БД.

        Yields:
            ApiUserRepository: репозиторий пользователей.
        """
        yield ApiUserRepository(db_session)

    @pytest_asyncio.fixture
    async def create_user(self, db_session):
        """
        Фикстура для создания пользователя.

        Args:
            db_session: фикстура для создания сессии БД.

        Yields:
            None
        """
        hashed_password = pwd_context.hash('test_password')
        await db_session.execute(
            insert(UserAlchemyModel).values(
                login='test_user',
                hashed_password=hashed_password,
            ),
        )
        yield
        await db_session.execute(
            delete(UserAlchemyModel).where(UserAlchemyModel.login == 'test_user'),  # noqa: E501
        )

    @pytest.mark.parametrize('username, password, expected', [
        pytest.param(
            'test_user',
            'test_password',
            True,
            id='user_found',
        ),
        pytest.param(
            'test_user',
            'wrong_password',
            False,
            id='wrong_password',
        ),
    ])
    async def test_check_user(
        self,
        db_session,
        repository,
        create_user,
        username,
        password,
        expected,
    ):
        """
        Тестирование метода проверки пользователя.

        Args:
            db_session: фикстура для создания сессии БД.
            repository: фикстура для создания репозитория пользователей.
            create_user: фикстура для создания пользователя.
            username (str): имя пользователя.
            password (str): пароль пользователя.
            expected: ожидаемый результат.

        """
        if not expected:  # noqa: WPS504
            with pytest.raises(HTTPException):
                await repository.check_user(username, password)
        else:
            assert await repository.check_user(username, password) == expected
