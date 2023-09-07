"""Schemas for the project."""
from decimal import Decimal

from pydantic import BaseModel


class UserBalanceRequest(BaseModel):
    """Balance response schema."""
    card_number: str
    balance: Decimal
