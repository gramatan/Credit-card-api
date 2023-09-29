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
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class CardAlchemyModel(Base):
    __tablename__ = 'cards'

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    card_number = Column(
        String(18),
        unique=True,
        nullable=False,
    )
    card_limit = Column(
        BigInteger,
        CheckConstraint('card_limit >= 0'),
        nullable=False,
    )
    card_balance = Column(
        BigInteger,
        nullable=False,
    )
    card_first_name = Column(
        String(50),
    )
    card_second_name = Column(
        String(50),
    )
    is_active = Column(
        Boolean,
        default=True,
    )


class CommonLogAlchemyModel(Base):
    __tablename__ = 'common_logs'

    card_number_id = Column(
        BigInteger,
        ForeignKey(
            'cards.id',
            ondelete='CASCADE',
        ),
        nullable=False,
    )
    datetime_utc = Column(
        DateTime,
        default=func.current_timestamp(),
        nullable=False,
    )
    limit_before = Column(
        BigInteger,
        nullable=False,
    )
    limit_after = Column(
        BigInteger,
        nullable=False,
    )
    changes = Column(
        BigInteger,
        nullable=False,
    )

    __table_args__ = (
        PrimaryKeyConstraint(
            'card_number_id',
            'datetime_utc',
        ),
    )


class BalanceLogAlchemyModel(Base):
    __tablename__ = 'balance_logs'

    card_number_id = Column(
        BigInteger,
        ForeignKey(
            'cards.id',
            ondelete='CASCADE',
        ),
        nullable=False,
    )
    datetime_utc = Column(
        DateTime,
        default=func.current_timestamp(),
        nullable=False,
    )
    balance_before = Column(
        BigInteger,
        nullable=False,
    )
    balance_after = Column(
        BigInteger,
        nullable=False,
    )
    changes = Column(
        BigInteger,
        nullable=False,
    )

    __table_args__ = (
        PrimaryKeyConstraint(
            'card_number_id',
            'datetime_utc',
        ),
    )
