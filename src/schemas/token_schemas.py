"""Schemas for the project."""
from pydantic import BaseModel


class TokenData(BaseModel):
    """Token data schema."""

    access_token: str
    token_type: str
