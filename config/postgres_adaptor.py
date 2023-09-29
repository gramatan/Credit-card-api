"""Модуль с адаптером для работы с БД."""
from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from config.postgres_config import app_config


class DatabaseConnection:
    """Класс для работы с БД."""

    def __init__(self, config: app_config):  # type: ignore
        """
        Инициализация класса.

        Args:
            config: Конфигурация.
        """
        engine = create_async_engine(
            url=config.postgres.uri,    # type: ignore
        )
        async_session_factory = async_sessionmaker(
            engine,
            expire_on_commit=False,
        )
        self._session_generator = async_scoped_session(
            async_session_factory,
            scopefunc=current_task,
        )

    def get_session(self) -> AsyncSession:
        """
        Получение сессии для работы с БД.

        Returns:
            Сессия для работы с БД.
        """
        return self._session_generator()


database_connection = DatabaseConnection(app_config)


async def get_db_session() -> AsyncSession:  # type: ignore
    """
    Получение сессии для работы с БД.

    Yields:
        Сессия для работы с БД.
    """
    async with database_connection.get_session() as session:
        yield session
