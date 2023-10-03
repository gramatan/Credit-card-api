"""Тесты хранилища логов."""
from datetime import datetime, timedelta

import pytest
import pytest_asyncio

from credit_card_balance.src.database.base import BalanceLogAlchemyModel
from credit_card_balance.src.repositories.log_storage import LogStorage


@pytest.mark.asyncio
class TestLogStorage:
    """Тесты хранилища логов."""

    @pytest_asyncio.fixture
    async def repository(self, db_session):
        """
        Фикстура для создания репозитория.

        Args:
            db_session (AsyncSession): Сессия для работы с БД.

        Yields:
            LogStorage: Репозиторий для тестов.
        """
        yield LogStorage(db_session)
        await db_session.commit()

    @pytest.mark.parametrize('card_id, from_date, to_date, expected_length', [
        pytest.param(
            '456',
            datetime(year=2024, month=2, day=29),
            datetime(year=2024, month=2, day=29, hour=23, minute=59),
            1,
            id='One day',
        ),
        pytest.param(
            '456',
            datetime(year=2023, month=8, day=31),
            datetime(year=2024, month=2, day=24),
            0,
            id='Before start of logs',
        ),
        pytest.param(
            '456',
            datetime(year=2024, month=3, day=6),
            datetime(year=2024, month=3, day=28),
            0,
            id='After end of logs',
        ),
        pytest.param(
            '456',
            datetime(year=2024, month=2, day=26),
            datetime(year=2024, month=2, day=28),
            3,
            id='Part of logs',
        ),
        pytest.param(
            '456',
            datetime(year=2024, month=2, day=25),
            datetime(year=2024, month=3, day=5),
            10,
            id='All logs',
        ),
        pytest.param(
            '3',
            datetime(year=2024, month=2, day=26),
            datetime(year=2024, month=2, day=28),
            0,
            id='No logs',
        ),
    ])
    async def test_get_balance_history(
        self,
        card_id,
        from_date,
        to_date,
        expected_length,
        repository,
    ):
        """
        Тест получения истории изменения баланса.

        Args:
            card_id (str): Номер карты.
            from_date (datetime): Начальная дата.
            to_date (datetime): Конечная дата.
            expected_length (int): Ожидаемая длина.
            repository (LogStorage): Репозиторий.
        """
        history = await repository.get_balance_history(
            card_id,
            from_date,
            to_date,
        )
        assert len(history) == expected_length

    @pytest.mark.parametrize('log_type, logs_count, expected_length', [
        pytest.param('balance_logs', 1, 1, id='save_log'),
    ])
    async def test_save_logs(   # noqa: WPS210
        self,
        log_type,
        logs_count,
        expected_length,
        repository,
    ):
        """
        Тест сохранения логов.

        Args:
            log_type (str): Тип логов.
            logs_count (int): Количество логов.
            expected_length (int): Ожидаемая длина.
            repository (LogStorage): Репозиторий.
        """
        logs = []
        prev = 0
        base_date = datetime(year=1989, month=5, day=10, minute=5)
        for addtional_day in range(logs_count):
            logs.append(BalanceLogAlchemyModel(
                card_number_id=2,
                datetime_utc=base_date + timedelta(minutes=addtional_day),
                balance_before=prev,
                balance_after=prev + 1000,
                changes=1000,
            ))
            prev += 1000

        for log in logs:
            await repository.save(log)

        response = await repository.get_balance_history(
            '456',
            datetime(year=1989, month=5, day=10),
            datetime(year=1989, month=5, day=11),
        )

        assert len(response) == expected_length
