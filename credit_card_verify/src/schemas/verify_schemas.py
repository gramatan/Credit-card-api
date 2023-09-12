"""Схема для ответа по верификации изображений."""
from pydantic import BaseModel


class VerificationResponse(BaseModel):
    """Схема для результата верификации."""

    verified: bool
