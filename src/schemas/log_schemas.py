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
    datetime_utc: datetime = datetime.utcnow()


class BalanceLogModel(LogBase):
    """Класс для логов баланса."""

    pass
