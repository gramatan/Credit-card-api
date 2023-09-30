"""Сервиис для работы с балансом пользователя."""
from datetime import datetime

from fastapi import Depends

from credit_card_balance.src.repositories.log_storage import LogStorage
from credit_card_balance.src.schemas.log_schemas import BalanceLogModel
from credit_card_balance.src.services.base_service import BaseService


class BalanceService(BaseService):
    """Сервис для работы с балансом пользователя."""

    def __init__(
        self,
        log_storage_repo: LogStorage = Depends(LogStorage),
    ):
        """
        Инициализация сервиса.

        Args:
            log_storage_repo (LogStorage): Репо транзакций.
        """
        self.logs = log_storage_repo

    async def get_balance_story(
        self,
        card_number: str,
        from_date: datetime,
        to_date: datetime,
    ) -> list[BalanceLogModel]:
        """
        Получение истории баланса.

        Args:
            card_number (str): Номер карты.
            from_date (datetime): Дата начала.
            to_date (datetime): Дата конца.

        Returns:
            list[BalanceLogModel]: История баланса.
        """
        balance_history = await self.logs.get_balance_history(
            card_number,
            from_date,
            to_date,
        )
        response: list[BalanceLogModel] = []

        if not balance_history:
            return response

        for log in balance_history:
            response.append(BalanceLogModel(
                card_number=card_number,
                before=self._kopecks_to_decimal(log.balance_before),
                after=self._kopecks_to_decimal(log.balance_after),
                changes=self._kopecks_to_decimal(log.changes),
                datetime_utc=log.datetime_utc,
            ))

        return response
