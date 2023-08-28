from dataclasses import dataclass
from decimal import Decimal


@dataclass
class User:
    card_number: str
    limit: Decimal
    info: dict
    _balance: Decimal = Decimal(0)

    @property
    def balance(self) -> Decimal:
        return self._balance

    @balance.setter
    def balance(self, value: Decimal):
        if value < -self.limit:
            raise ValueError('Баланс не может быть меньше лимита')
        self._balance = value
