"""Schemas for the project."""
from decimal import Decimal

from pydantic import BaseModel


class UserBase(BaseModel):
    """Базовый класс пользователей."""

    card_number: str
    limit: Decimal
    info: dict[str, str]


class UserBalance(UserBase):
    """Модель с балансом."""

    balance: Decimal
