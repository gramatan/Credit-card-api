"""Репозиторий для храненилища пользователей."""
from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from config.config import USER_EXISTS_ERROR, USER_NOT_FOUND_ERROR
from config.postgres_adaptor import get_db_session
from credit_card_balance.src.database.base import CardAlchemyModel


class UserStorage:
    """Класс для хранения пользователей."""

    def __init__(
        self,
        session: AsyncSession = Depends(get_db_session),
    ):
        """
        Инициализация репозитория.

        Args:
            session (AsyncSession): Сессия для работы с БД.
        """
        self.session = session

    async def add(self, card_number: str, user_info: dict) -> None:
        """
        Добавление пользователя.

        Args:
            card_number (str): Номер карты.
            user_info (dict): Информация о пользователе.

        Raises:
            ValueError: Если пользователь с такой картой уже существует.
        """
        user_info = user_info or {}
        user = CardAlchemyModel(
            card_number=card_number,
            card_limit=0,
            card_balance=0,
            card_first_name=user_info.get('first_name', ''),
            card_second_name=user_info.get('second_name', ''),
            is_active=True,
        )

        self.session.add(user)
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise ValueError(USER_EXISTS_ERROR)

    async def get_user(self, card_number: str) -> CardAlchemyModel | None:
        """
        Получение пользователя по номеру карты.

        Args:
            card_number (str): Номер карты.

        Returns:
            CardAlchemyModel | None: Пользователь.
        """
        db_user = await self.session.execute(
            select(
                CardAlchemyModel,
            ).filter_by(card_number=card_number),
        )
        return db_user.scalars().first()

    async def update_user(self, user: CardAlchemyModel) -> CardAlchemyModel:
        """
        Обновление пользователя.

        Args:
            user (CardAlchemyModel): Пользователь.

        Returns:
            CardAlchemyModel: Пользователь.

        Raises:
            ValueError: Если пользователь не существует.
        """
        is_exist_card = await self.get_user(user.card_number)
        if not is_exist_card:
            raise ValueError(USER_NOT_FOUND_ERROR)

        card_update = update(CardAlchemyModel).where(
            CardAlchemyModel.card_number == user.card_number,
        ).values(
            card_limit=user.card_limit,
            card_balance=user.card_balance,
            card_first_name=user.card_first_name,
            card_second_name=user.card_second_name,
        )
        await self.session.execute(card_update)
        await self.session.commit()

        return user

    async def close(self, card_number: str) -> bool:
        """
        Закрытие пользователя.

        Args:
            card_number (str): Номер карты.

        Returns:
            bool: True, если пользователь закрыт.

        Raises:
            ValueError: Если пользователь не существует или не активен.
        """
        user = await self.get_user(card_number)
        if not user:
            raise ValueError(USER_NOT_FOUND_ERROR)

        user.is_active = False
        await self.session.commit()

        return not user.is_active
