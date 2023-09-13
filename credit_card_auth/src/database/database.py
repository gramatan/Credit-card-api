"""База данных."""
from passlib.context import CryptContext

from config.config import TEST_USER_LOGIN, TEST_USER_PASSWORD

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

hashed_password = pwd_context.hash(TEST_USER_PASSWORD)
api_user = {'username': TEST_USER_LOGIN, 'password': hashed_password}
