"""Модель пользователя."""
from dataclasses import dataclass
from decimal import Decimal

from config.config import USER_BALANCE_LIMIT_ERROR


@dataclass
class User:
    """Класс для хранения информации о пользователе."""

    card_number: str
    limit: Decimal
    info: dict  # noqa: WPS110
    _balance: Decimal

    @property
    def balance(self) -> Decimal:
        """
        Геттер для баланса.

        Returns:
            Decimal: Баланс.
        """
        return self._balance

    @balance.setter
    def balance(self, new_value: Decimal):
        """
        Сеттер для баланса.

        Args:
            new_value (Decimal): Новый баланс.

        Raises:
            ValueError: Если новый баланс меньше лимита.
        """
        if new_value < -self.limit:
            raise ValueError(USER_BALANCE_LIMIT_ERROR)
        self._balance = new_value
