from decimal import Decimal

from src.models.user import User


class UserStorage:
    def __init__(self):
        self.active: dict[str, User] = {}
        self.closed: list[User] = []

    def add(self, card_number: str, info: dict) -> None:
        if self._is_exist_user(card_number, in_active=True, in_closed=True):
            raise ValueError(f'Пользователь с картой {card_number} уже существует')
        user = User(card_number=card_number, limit=Decimal(0), info=info)
        self.active[card_number] = user

    def get_user(self, card_number: str) -> User | None:
        user = self.active.get(card_number)
        if user:
            return user

        for user in self.closed:
            if user.card_number == card_number:
                user = user
                break
        return user

    def update_user(self, user: User) -> User:
        if not self._is_exist_user(user.card_number, in_active=True, in_closed=True):
            raise ValueError(f'Пользователя с картой {user.card_number} не существует')
        self.active[user.card_number] = user
        return user

    def close(self, card_number: str) -> bool:
        if not self._is_exist_user(card_number, in_active=True, in_closed=False):
            raise ValueError(f'Пользователь с картой {card_number} не активен или не существует')
        user = self.active.pop(card_number)
        self.closed.append(user)
        return user.card_number == self.closed[-1].card_number and user not in self.active

    def _is_exist_user(self, card_number: str, in_active: bool = True, in_closed: bool = True) -> bool:
        if in_active and card_number in self.active:
            return True
        if in_closed and any(user for user in self.closed if user.card_number == card_number):
            return True
        return False
