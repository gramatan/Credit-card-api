"""Schemas for the project."""
from decimal import Decimal

from pydantic import BaseModel


class BalanceResponse(BaseModel):
    """Balance response schema."""

    balance: Decimal
