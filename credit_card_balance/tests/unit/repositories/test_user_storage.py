"""Тесты для репозитория UserStorage."""

import pytest
import pytest_asyncio

from credit_card_balance.src.database.base import CardAlchemyModel
from credit_card_balance.src.repositories.user_storage import UserStorage


@pytest.mark.asyncio
class TestLogStorage:
    """Тесты для репозитория UserStorage."""

    @pytest_asyncio.fixture
    async def repository(self, db_session):
        """
        Фикстура для создания репозитория.

        Args:
            db_session (AsyncSession): Сессия для работы с БД.

        Yields:
            UserStorage: Репозиторий для тестов.
        """
        yield UserStorage(db_session)
        await db_session.commit()

    @pytest.mark.parametrize('card_number, user_info, expected', [
        pytest.param(
            '1234567890123456',
            {'name': 'John'},
            True,
            id='Add_new_user',
        ),
        pytest.param(
            '123',
            {'name': 'John'},
            'Raises',
            id='User already exist',
        ),
        pytest.param(
            '123456',
            None,
            True,
            id='Empty user info',
        ),
    ])
    async def test_add_success(
        self,
        card_number,
        user_info,
        expected,
        repository,
    ):
        """
        Тест для проверки добавления пользователя.

        Args:
            card_number (str): Номер карты.
            user_info (dict): Информация о пользователе.
            expected (bool): Ожидаемый результат.
            repository (UserStorage): репо с методами для проверки.
        """
        if expected == 'Raises':
            with pytest.raises(ValueError):
                await repository.add(card_number, user_info)
        else:
            await repository.add(card_number, user_info)
            check = await repository.get_user(card_number)
            assert expected == (check is not None)

    @pytest.mark.parametrize('card_number, expected_type, expected', [
        pytest.param('8675309', type(None), True, id='User exists'),
        pytest.param('123', CardAlchemyModel, True, id='User not exists'),
    ])
    async def test_get_user(
        self,
        card_number,
        expected_type,
        expected,
        repository,
    ):
        """
        Тест для проверки получения пользователя.

        Args:
            card_number (str): Номер карты.
            expected_type (type): Ожидаемый тип.
            expected (bool): Ожидаемый результат.
            repository (UserStorage): репо с методами для проверки.
        """
        test_result = await repository.get_user(card_number)
        assert isinstance(test_result, expected_type)

    @pytest.mark.parametrize('card_number, new_limit, expected_limit, exception', [  # noqa: E501
        pytest.param(
            '123',
            500,
            500,
            None,
            id='User exists',
        ),
        pytest.param(
            '8675309',
            500,
            None,
            'Raises',
            id='User not exists',
        ),
    ])
    async def test_update_user(
        self,
        card_number,
        new_limit,
        expected_limit,
        exception,
        repository,
    ):
        """
        Тест для проверки обновления пользователя.

        Args:
            card_number (str): Номер карты.
            new_limit (Decimal): Новый лимит.
            expected_limit (Decimal): Ожидаемый лимит.
            exception (str): Ожидаемое исключение.
            repository (UserStorage): репо с методами для проверки.
        """
        if exception == 'Raises':
            with pytest.raises(ValueError):
                user = CardAlchemyModel(
                    card_number=card_number,
                    card_limit=0,
                    card_balance=0,
                )
                await repository.update_user(user)
        else:
            user = await repository.get_user(card_number)
            user.card_limit = new_limit
            updated_user = await repository.update_user(user)
            assert updated_user.card_limit == expected_limit
            user_after = await repository.get_user(card_number)
            assert user_after.card_limit == expected_limit

    @pytest.mark.parametrize('card_number, expected', [
        pytest.param('123', True, id='User exists'),
        pytest.param('8675309', False, id='User not exists'),
    ])
    async def test_close(self, card_number, expected, repository):
        """
        Тест для проверки закрытия пользователя.

        Args:
            card_number (str): Номер карты.
            expected (bool): Ожидаемый результат.
            repository (UserStorage): репо с методами для проверки.
        """
        if not expected:    # noqa: WPS504
            with pytest.raises(ValueError):
                await repository.close(card_number)
        else:
            await repository.close(card_number)
            user = await repository.get_user(card_number)
            assert not user.is_active
