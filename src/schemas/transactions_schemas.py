"""Schemas for the project."""
from decimal import Decimal

from pydantic import BaseModel


class TransactionRequest(BaseModel):
    """Схема для транзакций."""

    card_number: str
    amount: Decimal


class UpdateUserInfoRequest(BaseModel):
    """Схема для обновления информации о пользователе."""

    card_number: str
    user_info: dict[str, str]


class ChangeLimitRequest(BaseModel):
    """Схема для изменения лимита."""

    card_number: str
    new_limit: Decimal
