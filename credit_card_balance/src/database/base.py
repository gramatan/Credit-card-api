"""Базовые модели для работы с БД."""
from datetime import datetime

import sqlalchemy.orm
from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    PrimaryKeyConstraint,
    String,
)
from sqlalchemy.sql import func

Base = sqlalchemy.orm.declarative_base()   # type: ignore


class CardAlchemyModel(Base):   # type: ignore
    """Модель карты."""

    __tablename__ = 'cards'

    id: int = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    card_number: str = Column(
        String(18),  # noqa: WPS432
        unique=True,
        nullable=False,
    )
    card_limit: int = Column(
        BigInteger,
        CheckConstraint('card_limit >= 0'),
        nullable=False,
    )
    card_balance: int = Column(
        BigInteger,
        nullable=False,
    )
    card_first_name: str = Column(
        String(50),  # noqa: WPS432
    )
    card_second_name: str = Column(
        String(50),  # noqa: WPS432
    )
    is_active: bool = Column(
        Boolean,
        default=True,
    )


class CommonLogAlchemyModel(Base):  # type: ignore
    """Модель лога изменения по карте."""

    __tablename__ = 'common_logs'

    card_number_id: int = Column(
        BigInteger,
        ForeignKey(
            'cards.id',
            ondelete='CASCADE',
        ),
        nullable=False,
    )
    datetime_utc: datetime = Column(
        DateTime,
        default=func.current_timestamp(),
        nullable=False,
    )
    limit_before: int = Column(
        BigInteger,
        nullable=False,
    )
    limit_after: int = Column(
        BigInteger,
        nullable=False,
    )
    changes: int = Column(
        BigInteger,
        nullable=False,
    )

    __table_args__ = (
        PrimaryKeyConstraint(
            'card_number_id',
            'datetime_utc',
        ),
    )


class BalanceLogAlchemyModel(Base):  # type: ignore
    """Модель лога изменения баланса по карте."""

    __tablename__ = 'balance_logs'

    card_number_id: int = Column(
        BigInteger,
        ForeignKey(
            'cards.id',
            ondelete='CASCADE',
        ),
        nullable=False,
    )
    datetime_utc: datetime = Column(
        DateTime,
        default=func.current_timestamp(),
        nullable=False,
    )
    balance_before: int = Column(
        BigInteger,
        nullable=False,
    )
    balance_after: int = Column(
        BigInteger,
        nullable=False,
    )
    changes: int = Column(
        BigInteger,
        nullable=False,
    )

    __table_args__ = (
        PrimaryKeyConstraint(
            'card_number_id',
            'datetime_utc',
        ),
    )
