"""База данных."""
from passlib.context import CryptContext

from src.repositories.log_storage import LogStorage
from src.repositories.transactions import Transactions
from src.repositories.user_storage import UserStorage

user_storage = UserStorage()
history = LogStorage()
db = Transactions(user_storage=user_storage, history=history)


def get_db():
    """
    Функция получения "базы данных".

    Returns:
        Transactions: "База данных".
    """
    user_storage.add('123', {'name': 'test'})
    return db


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

hashed_password = pwd_context.hash('test_password')
api_user = {'username': 'test_user', 'password': hashed_password}
