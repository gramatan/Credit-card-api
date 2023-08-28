from decimal import Decimal

from src.repositories.log_storage import LogStorage
from src.repositories.user_storage import UserStorage


class Transactions:
    def __init__(self, user_storage: UserStorage, history: LogStorage):
        self.user_storage = user_storage
        self.history = history

    def get_balance(self, card_number: str) -> Decimal | None:
        pass

    def withdraw(self, card_number: str, amount: Decimal) -> Decimal | None:
        pass

    def deposit(self, card_number: str, amount: Decimal) -> Decimal | None:
        pass

    def update_info(self, card_number: str, info: dict) -> dict | None:
        pass

    def change_limit(self, card_number: str, new_limit: Decimal) -> Decimal | None:
        pass

    def _change_balance(self, card_number: str, amount: Decimal) -> Decimal | None:
        pass

    def _check_amount(self, amount: Decimal) -> bool:
        pass
