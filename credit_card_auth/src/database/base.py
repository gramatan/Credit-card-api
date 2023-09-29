"""Базовые модели для работы с БД."""
from sqlalchemy import CHAR, VARCHAR, BigInteger, Column
from sqlalchemy.orm import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


class UserAlchemyModel(Base):  # type: ignore
    """Модель пользователя."""

    __tablename__ = 'users'

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    login = Column(
        VARCHAR(100),
        unique=True,
        nullable=False,
        index=True,
    )
    hashed_password = Column(
        CHAR(60),
        nullable=False,
    )
