"""Набор фикстур для тестов."""
import pytest

from src.repositories.user_storage import UserStorage


@pytest.fixture()
def not_empty_storage():
    """
    Фикстура для создания непустого хранилища.

    Yields:
        UserStorage: Хранилище c готовым пользователем.
    """
    storage = UserStorage()
    user_info = {'name': 'John'}
    card_number = '1234567890'
    storage.add(card_number, user_info)
    yield storage
