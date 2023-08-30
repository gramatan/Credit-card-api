"""Репозиторий для храненилища пользователей."""
from decimal import Decimal

from config.config import USER_EXISTS_ERROR, USER_NOT_FOUND_ERROR
from src.models.user import User


class UserStorage:
    """Класс для хранения пользователей."""

    def __init__(self):
        """Инициализация репозитория."""
        self.active: dict[str, User] = {}   # type: ignore
        self.closed: list[User] = []        # type: ignore

    def add(self, card_number: str, user_info: dict) -> None:
        """
        Добавление пользователя.

        Args:
            card_number (str): Номер карты.
            user_info (dict): Информация о пользователе.

        Raises:
            ValueError: Если пользователь с такой картой уже существует.
        """
        if self._is_exist_user(card_number, in_active=True, in_closed=True):
            raise ValueError(USER_EXISTS_ERROR)
        user = User(
            card_number=card_number,
            limit=Decimal(0),
            info=user_info,
            _balance=Decimal(0),
        )
        self.active[card_number] = user

    def get_user(self, card_number: str) -> User | None:
        """
        Получение пользователя по номеру карты.

        Args:
            card_number (str): Номер карты.

        Returns:
            User | None: Пользователь.
        """
        return self.active.get(card_number)

    def update_user(self, user: User) -> User:
        """
        Обновление пользователя.

        Args:
            user (User): Пользователь.

        Returns:
            User: Пользователь.

        Raises:
            ValueError: Если пользователь не существует.
        """
        if not self._is_exist_user(     # noqa: WPS337
            user.card_number,
            in_active=True,
            in_closed=False,
        ):
            raise ValueError(USER_NOT_FOUND_ERROR)
        self.active[user.card_number] = user
        return user

    def close(self, card_number: str) -> bool:
        """
        Закрытие пользователя.

        Args:
            card_number (str): Номер карты.

        Returns:
            bool: True, если пользователь закрыт.

        Raises:
            ValueError: Если пользователь не существует или не активен.
        """
        if not self._is_exist_user(     # noqa: WPS337
            card_number,
            in_active=True,
            in_closed=False,
        ):
            raise ValueError(USER_NOT_FOUND_ERROR)
        self.closed.append(self.active.pop(card_number))
        return card_number not in self.active

    def _is_exist_user(
        self,
        card_number: str,
        in_active: bool = True,
        in_closed: bool = True,
    ) -> bool:
        """
        Проверка существования пользователя.

        Args:
            card_number (str): Номер карты.
            in_active (bool): Проверять в активных.
            in_closed (bool): Проверять в закрытых.

        Returns:
            bool: True, если пользователь существует.
        """
        in_active_condition = in_active and card_number in self.active
        in_closed_condition = in_closed and any(
            user for user in self.closed if user.card_number == card_number
        )

        return in_active_condition or in_closed_condition
