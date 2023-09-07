"""База данных."""
from passlib.context import CryptContext  # type: ignore

from src.repositories.log_storage import LogStorage
from src.repositories.transactions import Transactions
from src.repositories.user_storage import UserStorage

user_storage = UserStorage()
history = LogStorage()
db = Transactions(user_storage=user_storage, history=history)
user_storage.add('123', {'name': 'test'})


def get_db():
    """
    Функция получения "базы данных".

    Returns:
        tuple[Transactions, UserStorage, LogStorage]: "База данных".
    """
    return db, user_storage, history


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

hashed_password = pwd_context.hash('test_password')
api_user = {'username': 'test_user', 'password': hashed_password}
