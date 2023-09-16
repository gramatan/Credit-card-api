"""Конфигурационный файл приложения."""

SECRET_KEY = '27946a0b61bb4f8b3d7613c012e8badb0fd28d6fb79f2286de87c3bed42d143b'  # noqa: S105, E501
ALGORITHM = 'HS256'
TOKEN_TTL = 30

USER_EXISTS_ERROR = 'Пользователь с таким номером карты уже существует'
USER_NOT_FOUND_ERROR = 'Пользователь с таким номером карты не найден'
USER_LIMIT_ERROR = 'Нельзя установить лимит меньше нуля'
USER_BALANCE_ERROR = 'Нельзя установить баланс меньше нуля'
USER_BALANCE_LIMIT_ERROR = 'Нельзя установить баланс меньше лимита'
AMOUNT_ERROR = 'Некореектная сумма операции'

VERIFIED_BALANCE = 100000
UNVERIFIED_BALANCE = 20000

AUTH_APP_PORT = 24001
BALANCE_APP_PORT = 24101
VERIFICATION_PORT = 24201
KAFKA_PORT = 24301

AUTH_APP_HOST = '127.0.0.1'
BALANCE_APP_HOST = '127.0.0.1'
VERIFICATION_HOST = '127.0.0.1'
KAFKA_HOST = '127.0.0.1'

PATH_PREFIX = '/api'

RESPONSE_TIMEOUT = 30

PRE_INSTALLED_CARD_NUMBER = '123'
PRE_INSTALLED_CARD_DATA = {             # noqa: WPS407
    'name': 'test',
}

TEST_USER_LOGIN = 'test_user'
TEST_USER_PASSWORD = 'test_password'    # noqa: S105
