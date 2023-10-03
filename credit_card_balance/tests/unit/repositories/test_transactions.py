"""Тесты для репозитория транзакций."""
import pytest
import pytest_asyncio

from credit_card_balance.src.repositories.log_storage import LogStorage
from credit_card_balance.src.repositories.transactions import Transactions
from credit_card_balance.src.repositories.user_storage import UserStorage


@pytest.mark.asyncio
class TestTransactions:
    """Тесты для репозитория транзакций."""

    GOOD_USER = '123'       # noqa: WPS115
    BAD_USER = '8675309'    # noqa: WPS115

    @pytest_asyncio.fixture
    async def repository(self, db_session):
        """
        Фикстура для создания репозитория.

        Args:
            db_session (AsyncSession): Сессия для работы с БД.

        Yields:
            Transactions: Репозиторий для тестов.
        """
        yield Transactions(UserStorage(db_session), LogStorage(db_session))
        await db_session.commit()

    @pytest.mark.parametrize('card_id, expected_balance, exception', [
        pytest.param(
            GOOD_USER,
            0,
            None,
            id='User exists',
        ),
        pytest.param(
            BAD_USER,
            None,
            'Raises',
            id='User not exists',
        ),
    ])
    async def test_get_balance(
        self,
        card_id,
        expected_balance,
        exception,
        repository,
    ):
        """
        Тест метода получения баланса.

        Args:
            card_id (str): Номер карты.
            expected_balance (int): Ожидаемый баланс.
            exception (str): Ожидаемое исключение.
            repository (Transactions): репо с методами для проверки.
        """
        if exception == 'Raises':
            with pytest.raises(ValueError):
                await repository.get_balance(card_id)
        else:
            test_result = await repository.get_balance(card_id)
            assert test_result == expected_balance

    @pytest.mark.parametrize('card_id, amount, expected_balance, exception', [
        pytest.param(
            GOOD_USER,
            50,
            -50,
            None,
            id='Valid',
        ),
        pytest.param(
            GOOD_USER,
            0,
            None,
            'Raises',
            id='Invalid amount',
        ),
        pytest.param(
            BAD_USER,
            50,
            None,
            'Raises',
            id='User not exists',
        ),
        pytest.param(
            GOOD_USER,
            5000,
            None,
            'Raises',
            id='Withdrawal amount > balance',
        ),
    ])
    async def test_withdraw(
        self,
        card_id,
        amount,
        expected_balance,
        exception,
        repository,
    ):
        """
        Тест метода снятия денег.

        Args:
            card_id (str): Номер карты.
            amount (int): Сумма.
            expected_balance (Decimal): Ожидаемый баланс.
            exception (str): Ожидаемое исключение.
            repository (Transactions): репо с методами для проверки.
        """
        if exception == 'Raises':
            with pytest.raises(ValueError):
                await repository.withdraw(card_id, amount)
        else:
            await repository.withdraw(card_id, amount)
            assert await repository.get_balance(card_id) == expected_balance

    @pytest.mark.parametrize('card_id, amount, exception', [
        pytest.param(
            GOOD_USER,
            50,
            None,
            id='Valid',
        ),
        pytest.param(
            GOOD_USER,
            0,
            'Raises',
            id='Invalid amount',
        ),
        pytest.param(
            BAD_USER,
            50,
            'Raises',
            id='User not exists',
        ),
    ])
    async def test_deposit(
        self,
        card_id,
        amount,
        exception,
        repository,
    ):
        """
        Тест метода пополнения баланса.

        Args:
            card_id (str): Номер карты.
            amount (int): Сумма.
            exception (str): Ожидаемое исключение.
            repository (Transactions): репо с методами для проверки.
        """
        if exception == 'Raises':
            with pytest.raises(ValueError):
                await repository.deposit(card_id, amount)
        else:
            current = await repository.get_balance(card_id)
            await repository.deposit(card_id, amount)
            assert await repository.get_balance(card_id) == current + amount

    @pytest.mark.parametrize('card_id, new_limit, expected_limit, exception', [
        pytest.param(
            GOOD_USER,
            2000,
            2000,
            None,
            id='Valid',
        ),
        pytest.param(
            GOOD_USER,
            -1,
            None,
            'Raises',
            id='Invalid amount',
        ),
        pytest.param(
            BAD_USER,
            2000,
            None,
            'Raises',
            id='User not exists',
        ),
    ])
    async def test_change_limit(  # noqa: WPS211
        self,
        card_id,
        new_limit,
        expected_limit,
        exception,
        repository,
    ):
        """
        Тест метода изменения лимита.

        Args:
            card_id (str): Номер карты.
            new_limit (int): Новый лимит.
            expected_limit (int): Ожидаемый лимит.
            exception (str): Ожидаемое исключение.
            repository (Transactions): репо с методами для проверки.
        """
        if exception == 'Raises':
            with pytest.raises(ValueError):
                await repository.change_limit(card_id, new_limit)
        else:
            await repository.change_limit(card_id, new_limit)
            user = await repository._user_storage.get_user(card_id)
            assert user.card_limit == expected_limit

    @pytest.mark.parametrize('card_id, new_info, expected_info, exception', [
        pytest.param(
            GOOD_USER,
            {'name': 'Not a John', 'surname': 'Ivanov'},
            {'name': 'Not a John', 'surname': 'Ivanov'},
            None,
            id='Update existed info and add new',
        ),
        pytest.param(
            GOOD_USER,
            {'name': 'Not a John'},
            {'name': 'Not a John'},
            None,
            id='Update existed info only',
        ),
        pytest.param(
            BAD_USER,
            {'name': 'Not a John'},
            None,
            'Raises',
            id='User not exists',
        ),
    ])
    async def test_update_info(
        self,
        card_id,
        new_info,
        expected_info,
        exception,
        repository,
    ):
        """
        Тест метода обновления информации о пользователе.

        Args:
            card_id (str): Номер карты.
            new_info (dict): Новая информация.
            expected_info (dict): Ожидаемая информация.
            exception (str): Ожидаемое исключение.
            repository (Transactions): репо с методами для проверки.
        """
        if exception == 'Raises':
            with pytest.raises(ValueError):
                await repository.update_info(card_id, new_info)
            return

        await repository.update_info(card_id, new_info)

        user = await repository._user_storage.get_user(card_id)
        if expected_info.get('name'):
            assert user.card_first_name == expected_info['name']
        if expected_info.get('surname'):
            assert user.card_second_name == expected_info['surname']
