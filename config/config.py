"""Конфигурационный файл приложения."""

SECRET_KEY = '27946a0b61bb4f8b3d7613c012e8badb0fd28d6fb79f2286de87c3bed42d143b'  # noqa: S105, E501
ALGORITHM = 'HS256'
TOKEN_TTL = 30

USER_EXISTS_ERROR = 'Пользователь с таким номером карты уже существует'
USER_NOT_FOUND_ERROR = 'Пользователь с таким номером карты не найден'
USER_LIMIT_ERROR = 'Нельзя установить лимит меньше нуля'
USER_BALANCE_ERROR = 'Нельзя установить баланс меньше нуля'
USER_BALANCE_LIMIT_ERROR = 'Нельзя установить баланс меньше лимита'
