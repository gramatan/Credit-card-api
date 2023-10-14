"""Конфигурационный файл приложения."""
import os

USER_EXISTS_ERROR = 'Пользователь с таким номером карты уже существует'
USER_NOT_FOUND_ERROR = 'Пользователь с таким номером карты не найден'
USER_LIMIT_ERROR = 'Нельзя установить лимит меньше нуля'
USER_BALANCE_ERROR = 'Нельзя установить баланс меньше нуля'
USER_BALANCE_LIMIT_ERROR = 'Нельзя установить баланс меньше лимита'
AMOUNT_ERROR = 'Некореектная сумма операции'

VERIFIED_BALANCE = int(os.environ.get('VERIFIED_BALANCE', 100000))
UNVERIFIED_BALANCE = int(os.environ.get('UNVERIFIED_BALANCE', 20000))

FIRST_USER_FIELD = os.environ.get('FIRST_USER_FIELD', 'name')
SECOND_USER_FIELD = os.environ.get('SECOND_USER_FIELD', 'surname')

SECRET_KEY = os.environ.get('SECRET_KEY', '27946a0b61bb4f8b3d7613c012e8badb0fd28d6fb79f2286de87c3bed42d143b')
ALGORITHM = os.environ.get('ALGORITHM', 'HS256')
TOKEN_TTL = int(os.environ.get('TOKEN_TTL', 30))

AUTH_APP_PORT = int(os.environ.get('AUTH_APP_PORT', 24001))
BALANCE_APP_PORT = int(os.environ.get('BALANCE_APP_PORT', 24101))
VERIFICATION_PORT = int(os.environ.get('VERIFICATION_PORT', 24201))

AUTH_APP_HOST = os.environ.get('AUTH_APP_HOST', 'cc_auth')
BALANCE_APP_HOST = os.environ.get('BALANCE_APP_HOST', 'cc_balance')
VERIFICATION_HOST = os.environ.get('VERIFICATION_HOST', 'cc_verify')

KAFKA_HOST = os.environ.get('KAFKA_HOST', 'cc_kafka')
KAFKA_PORT = int(os.environ.get('KAFKA_PORT', 9092))
KAFKA_USER = os.environ.get('KAFKA_USER', '')
KAFKA_PASSWORD = os.environ.get('KAFKA_PASSWORD', '')

POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'cc_postgres')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')

POSTGRES_DB_USER = os.environ.get('POSTGRES_DB_USER', 'shift_cc')
POSTGRES_DB_PASS = os.environ.get('POSTGRES_DB_PASS', 'shift_cc_pass')
POSTGRES_DB_NAME = os.environ.get('POSTGRES_DB_NAME', 'shift_cc_db')

PATH_PREFIX = '/api'
RESPONSE_TIMEOUT = int(os.environ.get('RESPONSE_TIMEOUT', 10))
PRE_INSTALLED_CARD_NUMBER = '123'
PRE_INSTALLED_CARD_DATA = {'name': 'test'}

TEST_USER_LOGIN = os.environ.get('TEST_USER_LOGIN', 'test_user')
TEST_USER_PASSWORD = os.environ.get('TEST_USER_PASSWORD', 'test_password')
