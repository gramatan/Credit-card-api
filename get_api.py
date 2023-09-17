"""Скрипт для генерации документации по API."""
import os

import yaml  # type: ignore

from main_auth import app as auth_app
from main_balance import app as balance_app

if __name__ == '__main__':
    if not os.path.exists('docs'):
        os.mkdir('docs')

    with open('docs/cc_auth.yaml', 'w', encoding='utf-8') as auth_api_file:
        yaml.dump(auth_app.openapi(), auth_api_file, allow_unicode=True)

    with open('docs/cc_balance.yaml', 'w', encoding='utf-8') as b_api_file:
        yaml.dump(balance_app.openapi(), b_api_file, allow_unicode=True)
