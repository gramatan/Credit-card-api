"""Schemas for the project."""
from decimal import Decimal

from pydantic import BaseModel


class TransactionRequest(BaseModel):
    """Схема для транзакций."""

    card_number: str
    balance: Decimal


class VerificationRequest(BaseModel):
    """Схема для результата верификации."""

    verified: bool
