"""Репозиторий для хранения логов."""
from datetime import datetime

from fastapi import Depends
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from config.postgres_adaptor import get_db_session
from credit_card_balance.src.database.base import (
    BalanceLogAlchemyModel,
    CardAlchemyModel,
    CommonLogAlchemyModel,
)


class LogStorage:
    """Репозиторий для хранения логов."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        """
        Инициализация репозитория.

        Args:
            session (AsyncSession): Сессия для работы с БД.
        """
        self.session = session

    async def save(
        self,
        log: CommonLogAlchemyModel | BalanceLogAlchemyModel,
    ) -> None:
        """
        Сохранение лога.

        Args:
            log: Лог (может быть или BalanceLog, или CommonLog).
        """
        self.session.add(log)
        await self.session.commit()

    async def get_balance_history(
        self,
        card_number: str,
        from_date: datetime,
        to_date: datetime,
    ) -> list[BalanceLogAlchemyModel]:
        """
        Получение истории изменения баланса.

        Args:
            card_number (str): Номер карты.
            from_date (datetime): Начальная дата.
            to_date (datetime): Конечная дата.

        Returns:
            list[BalanceLogAlchemyModel]: История изменения баланса.
        """
        card = await self.session.execute(
            select(CardAlchemyModel).filter_by(card_number=card_number),
        )
        card = card.scalar_one_or_none()    # type: ignore
        if not card:
            return []

        logs = await self.session.execute(
            select(
                BalanceLogAlchemyModel,
            ).filter(
                BalanceLogAlchemyModel.card_number_id == card.id,   # type: ignore # noqa: E501
                and_(
                    BalanceLogAlchemyModel.datetime_utc >= from_date,
                    BalanceLogAlchemyModel.datetime_utc <= to_date,
                ),
            ).order_by(
                BalanceLogAlchemyModel.datetime_utc.desc(),
            ),
        )
        return list(logs.scalars().all())
