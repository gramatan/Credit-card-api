"""База данных."""
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
