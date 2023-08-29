from bisect import bisect_left, bisect_right
from collections import defaultdict
from datetime import datetime

from src.models.logs import BalanceLog, CommonLog


class LogStorage:
    def __init__(self):
        self._balance_logs: defaultdict[str, list[BalanceLog]] = defaultdict(list)
        self._other_logs: list[CommonLog] = []

    def save(self, log: CommonLog):
        if isinstance(log, BalanceLog):
            if log.card_number in self._balance_logs:
                self._balance_logs[log.card_number].append(log)
            else:
                self._balance_logs[log.card_number] = [log]
        else:
            self._other_logs.append(log)

    def get_balance_history(self, card_number: str, from_date: datetime, to_date: datetime) -> list[BalanceLog]:
        logs = self._balance_logs.get(card_number, [])

        if logs:
            start_date = bisect_left(logs, from_date)
            end_date = bisect_right(logs, to_date)

            return logs[start_date:end_date]
        return []

    def _get_datetime_from_log(self, log: BalanceLog):
        return log.datetime_utc
