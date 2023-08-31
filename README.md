## Тесты для компонентов истории и транзакций.

Добавлены тесты для компонентов истории и транзакций.
  - `tests/`
    - `unit/` : Юнит тесты разбиты по файлам в соответствии со структурой проекта.
    - [test_log_storage.py](tests%2Funit%2Frepositories%2Ftest_log_storage.py)
    - [test_user_storage.py](tests%2Funit%2Frepositories%2Ftest_user_storage.py)
    - [test_transactions.py](tests%2Funit%2Frepositories%2Ftest_transactions.py)
  - `tests/`
    - `integration/` : Сценарий интеграционных тестов из задания в одном файле. 
    - [test_main_scenario.py](tests%2Fintegration%2Ftest_main_scenario.py)\
    

## Написать классы компонентов истории и транзакций в соответствии со схемами.

Добавлены классы компонентов истории и транзакций в соответствии со схемами.
  - `models/`
    - [user.py](src%2Fmodels%2Fuser.py) : Модель пользователя.
    - [logs.py](src%2Fmodels%2Flogs.py) : Модель логов.
  - `repositories/`
    - [user_storage.py](src%2Frepositories%2Fuser_storage.py) : Репозиторий для работы с хранилищем пользователей.
    - [log_storage.py](src%2Frepositories%2Flog_storage.py) : Репозиторий для работы с хранилищем логов.
    - [transactions.py](src%2Frepositories%2Ftransactions.py) : Репозиторий для работы транзакциями.


## Credit card api.


---
# Оглавление
1. TBU

## Описание файлов проекта и инструкция по запуску сервиса:

[CONTRIBUTING.md](CONTRIBUTING.md)

## Проверка работоспособности сервиса

Откройте веб-браузер и перейдите по адресу `http://localhost:8000`. Вы должны увидеть ответ от вашего приложения.
Данные предустановленного пользователя:
```
логин: test_user
пароль: test_password
```

## Просмотр автоматически сгенерированной документации FastAPI

FastAPI автоматически генерирует документацию для вашего API. Чтобы просмотреть её, перейдите по адресу `http://localhost:8000/docs` в вашем браузере.

# Описание API

## Эндпоинты

### `POST /token`

Этот эндпоинт предназначен для получения токена доступа. В теле запроса необходимо передать следующие параметры:

- `username`: Имя пользователя.
- `password`: Пароль пользователя.

При успешном выполнении запроса сервер вернёт объект с токеном доступа.
