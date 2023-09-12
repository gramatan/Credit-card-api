"""Модуль содержит классы для логирования изменений по карте."""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class CommonLog:
    """Базовый класс для логирования."""

    card_number: str
    before: Decimal
    after: Decimal
    changes: Decimal
    _datetime_utc: datetime

    @property
    def datetime_utc(self):
        """
        Геттер для времени в UTC.

        Returns:
            datetime: Время в UTC.
        """
        return self._datetime_utc

    @datetime_utc.setter
    def datetime_utc(self, new_time: datetime):
        """
        Сеттер для времени в UTC.

        Args:
            new_time: Время в UTC.
        """
        self._datetime_utc = new_time


@dataclass
class BalanceLog(CommonLog):
    """Класс для логирования изменений баланса."""

    before: Decimal
    after: Decimal
    changes: Decimal
