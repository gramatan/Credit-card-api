from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class BalanceLog:
    before: Decimal
    after: Decimal
    changes: Decimal


@dataclass
class CommonLog:
    card_number: str
    before: Decimal
    after: Decimal
    changes: Decimal
    _datetime_utc: datetime
