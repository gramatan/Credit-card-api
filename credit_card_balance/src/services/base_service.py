"""Класс для базового сервиса."""
from decimal import Decimal


class BaseService:
    """Базовый сервис."""

    def _decimal_to_kopecks(self, amount: Decimal) -> int:
        """
        Перевод Decimal в копейки.

        Args:
            amount (Decimal): Сумма.

        Returns:
            int: Сумма в копейках.
        """
        return int(amount * 100)

    def _kopecks_to_decimal(self, amount: int) -> Decimal:
        """
        Перевод копеек в Decimal.

        Args:
            amount (int): Сумма в копейках.

        Returns:
            Decimal: Сумма.
        """
        return Decimal(amount) / 100
