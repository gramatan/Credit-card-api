from collections import defaultdict
from datetime import datetime

from src.models.logs import BalanceLog, CommonLog


class LogStorage:
    def __init__(self):
        self.balance_logs: defaultdict[str, list[BalanceLog]] = defaultdict(list)
        self.other_logs: list[CommonLog] = []

    def save_log(self, card_number: str, log: BalanceLog | CommonLog) -> None:
        if isinstance(log, BalanceLog):
            self.balance_logs[card_number].append(log)
        else:
            self.other_logs.append(log)

    def get_balance_history(self, card_number: str, from_datetime: datetime, to_datetime: datetime) -> list[BalanceLog]:
        return [log for log in self.balance_logs.get(card_number, []) if from_datetime <= log._datetime_utc <= to_datetime]
