from sqlalchemy import Column, BigInteger, VARCHAR, CHAR
from sqlalchemy.orm import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


class UserAlchemyModel(Base):
    __tablename__ = 'users'

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        index=True,
    )
    login = Column(
        VARCHAR,
        unique=True,
        nullable=False,
        index=True,
        length=100,
    )
    hashed_password = Column(
        CHAR,
        nullable=False,
        length=60,
    )
