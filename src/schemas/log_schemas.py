"""Schemas for the project."""
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class LogBase(BaseModel):
    """Базовый класс для логов."""

    card_number: str
    before: Decimal
    after: Decimal
    changes: Decimal
    datetime_utc: datetime


class BalanceLogModel(LogBase):
    """
    Класс для логов баланса.

    Может быть изменен в дальнейшем.
    """

    pass    # noqa: WPS420, WPS604, WPS30
