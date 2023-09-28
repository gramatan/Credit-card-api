from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from config.postgres_config import app_config


class DatabaseConnection:

    def __init__(self, config: app_config):
        _engine = create_async_engine(
            url=config.postgres.uri,
        )
        async_session_factory = async_sessionmaker(
            _engine,
            expire_on_commit=False,
        )
        self._session_generator = async_scoped_session(
            async_session_factory,
            scopefunc=current_task,
        )

    def get_session(self) -> AsyncSession:
        return self._session_generator()
