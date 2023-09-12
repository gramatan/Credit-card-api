"""Репозиторий для хранения логов."""
from bisect import bisect_left, bisect_right
from collections import defaultdict
from datetime import datetime

from credit_card_auth.src.models.logs import BalanceLog, CommonLog

BalanceLogDict = dict[str, list[BalanceLog]]


class LogStorage:
    """Репозиторий для хранения логов."""

    def __init__(self):
        """Инициализация репозитория."""
        self._balance_logs: BalanceLogDict = defaultdict(list)  # type: ignore
        self._other_logs: list[CommonLog] = []  # type: ignore

    def save(self, log: CommonLog):
        """
        Сохранение лога.

        Args:
            log (CommonLog): Лог.
        """
        if isinstance(log, BalanceLog):
            logs = self._balance_logs.get(log.card_number)
            if logs is None:
                self._balance_logs[log.card_number] = [log]
            else:
                logs.append(log)
        else:
            self._other_logs.append(log)

    def get_balance_history(
        self,
        card_number: str,
        from_date: datetime,
        to_date: datetime,
    ) -> list[BalanceLog]:
        """
        Получение истории изменения баланса.

        Args:
            card_number (str): Номер карты.
            from_date (datetime): Начальная дата.
            to_date (datetime): Конечная дата.

        Returns:
            list[BalanceLog]: История изменения баланса.
        """
        logs = self._balance_logs.get(card_number, [])

        if logs:
            start_date = bisect_left(
                logs,
                from_date,
                key=self._get_datetime_from_log,
            )
            end_date = bisect_right(
                logs,
                to_date,
                key=self._get_datetime_from_log,
            )

            return logs[start_date:end_date]
        return []

    def _get_datetime_from_log(
        self,
        log: BalanceLog,
    ):
        """
        Получение даты из лога.

        Args:
            log (BalanceLog): Лог.

        Returns:
            datetime: Дата.
        """
        return log.datetime_utc
