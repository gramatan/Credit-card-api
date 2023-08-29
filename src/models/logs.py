from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class CommonLog:
    card_number: str
    before: Decimal
    after: Decimal
    changes: Decimal
    _datetime_utc: datetime

    @property
    def datetime_utc(self):
        return self._datetime_utc

    @datetime_utc.setter
    def datetime_utc(self, value: datetime):
        self._datetime_utc = value


@dataclass
class BalanceLog(CommonLog):
    before: Decimal
    after: Decimal
    changes: Decimal
