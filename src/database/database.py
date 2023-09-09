"""База данных."""
from passlib.context import CryptContext  # type: ignore

from config.config import (
    PRE_INSTALLED_CARD_DATA,
    PRE_INSTALLED_CARD_NUMBER,
    TEST_USER_LOGIN,
    TEST_USER_PASSWORD,
)
from src.repositories.log_storage import LogStorage
from src.repositories.transactions import Transactions
from src.repositories.user_storage import UserStorage

user_storage = UserStorage()
history = LogStorage()
db = Transactions(user_storage=user_storage, history=history)
user_storage.add(
    PRE_INSTALLED_CARD_NUMBER,
    PRE_INSTALLED_CARD_DATA,
)


def get_db():
    """
    Функция получения "базы данных".

    Returns:
        tuple[Transactions, UserStorage, LogStorage]: "База данных".
    """
    return db, user_storage, history


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

hashed_password = pwd_context.hash(TEST_USER_PASSWORD)
api_user = {'username': TEST_USER_LOGIN, 'password': hashed_password}
