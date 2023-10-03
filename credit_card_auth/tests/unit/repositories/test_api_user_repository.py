import pytest
import pytest_asyncio
from fastapi import HTTPException
from sqlalchemy import delete, insert

from credit_card_auth.src.database.base import UserAlchemyModel, pwd_context
from credit_card_auth.src.repositories.api_user_repository import (
    ApiUserRepository,
)


@pytest.mark.asyncio
class TestUserRepository:

    @pytest_asyncio.fixture
    async def repository(self, db_session):
        yield ApiUserRepository(db_session)

    @pytest_asyncio.fixture
    async def create_user(self, db_session):
        hashed_password = pwd_context.hash('test_password')
        await db_session.execute(
            insert(UserAlchemyModel).values(
                login='test_user',
                hashed_password=hashed_password,
            ),
        )
        yield
        await db_session.execute(
            delete(UserAlchemyModel).where(UserAlchemyModel.login == 'test_user'),
        )

    @pytest.mark.parametrize('username, password, result', [
        pytest.param(
            'test_user',
            'test_password',
            True,
            id='user_found',
        ),
        pytest.param(
            'test_user',
            'wrong_password',
            False,
            id='wrong_password',
        ),
    ])
    async def test_check_user(
            self,
            db_session,
            repository,
            create_user,
            username,
            password,
            result,
    ):
        if result == False:
            with pytest.raises(HTTPException):
                await repository.check_user(username, password)
        else:
            assert await repository.check_user(username, password) == result
