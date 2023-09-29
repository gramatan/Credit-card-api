"""Add test data

Revision ID: 66e2e1b7375a
Revises: 82b113162ce5
Create Date: 2023-09-29 13:13:53.693624

"""
from typing import Sequence, Union

from passlib.context import CryptContext
from alembic import op
import sqlalchemy as sa


TEST_USER_LOGIN = "test_user"
TEST_USER_PASSWORD = "test_password"
TEST_CARD_NUMBER = "123"
TEST_FIRST_NAME = "test"


# revision identifiers, used by Alembic.
revision: str = '66e2e1b7375a'
down_revision: Union[str, None] = '82b113162ce5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    hashed_password = pwd_context.hash(TEST_USER_PASSWORD)

    op.execute(
        sa.text(
            """
            INSERT INTO users (login, hashed_password)
            VALUES (:login, :hashed_password)
            """
        ).bindparams(login=TEST_USER_LOGIN, hashed_password=hashed_password)
    )

    op.execute(
        sa.text(
            """
            INSERT INTO cards (card_number, card_limit, card_balance, card_first_name)
            VALUES (:card_number, 0, 0, :card_first_name)
            """
        ).bindparams(card_number=TEST_CARD_NUMBER, card_first_name=TEST_FIRST_NAME)
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            """
            DELETE FROM common_logs
            WHERE card_number_id = (SELECT id FROM cards WHERE card_number = :card_number)
            """
        ).bindparams(card_number=TEST_CARD_NUMBER)
    )

    op.execute(
        sa.text(
            """
            DELETE FROM balance_logs
            WHERE card_number_id = (SELECT id FROM cards WHERE card_number = :card_number)
            """
        ).bindparams(card_number=TEST_CARD_NUMBER)
    )

    op.execute(
        sa.text(
            """
            DELETE FROM cards WHERE card_number = :card_number
            """
        ).bindparams(card_number=TEST_CARD_NUMBER)
    )

    op.execute(
        sa.text(
            """
            DELETE FROM users WHERE login = :login
            """
        ).bindparams(login=TEST_USER_LOGIN)
    )

