"""Schemas for the project."""
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class BalanceLogModel(BaseModel):
    """Класс для логов баланса."""

    card_number: str
    before: Decimal
    after: Decimal
    changes: Decimal
    datetime_utc: datetime
