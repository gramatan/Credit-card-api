# Вклад в проект "Shift Rest"

## Введение

Этот файл предназначен для разработчиков, которые хотят внести свой вклад в проект. Здесь вы найдете информацию о том, как настроить проект для разработки, структуру проекта, а также рекомендации и требования по стилю кода.

## Сетап для разработки

1. Клонируйте репозиторий:
```
git clone [ссылка на ВАШ форк этого репозитория]
```

2. Перейдите в директорию проекта:
```
cd credit_card
```

3. Установите все зависимости с помощью [Poetry](https://python-poetry.org/):
```
poetry install
```

4. Активация виртуального окружение для запуска приложения или flake8, mypy и pytest:
```
poetry shell
```

5. Запуск приложения:

    Запуск без докера(приложение будет запущено на 24001 порту локальной машины):
    ```
    python main.py
    ```

   Запуск в докере: - TBU


## Структура проекта

- [main.py](main.py) : Основной файл приложения.
- `config/`[config.py](config%2Fconfig.py) : Файл с константами для приложения.
  - APP_PORT : Порт, на котором будет запущено приложение.
  - APP_HOST : Хост приложения.
  - PRE_INSTALLED_CARD_NUMBER : Номер карты, который будет добавлен при первоначальной инициализации приложения для тестирования.
  - PRE_INSTALLED_CARD_DATA: Данные карты^
  - TEST_USER_LOGIN: Логин предустановленного пользователя.
  - TEST_USER_PASSWORD: Пароль предустановленного пользователя.


- `src` : Исходный код проекта.
  - [database](src%2Fdatabase) : Файлы для работы с базой данных.  - TBU
  - `models/` : Модели данных.
    - [user.py](src%2Fmodels%2Fuser.py) : Модель пользователя.
    - [logs.py](src%2Fmodels%2Flogs.py) : Модель логов.
  - `repositories/` : Файлы с репозиториями для работы с базой данных.
    - [user_storage.py](src%2Frepositories%2Fuser_storage.py) : Репозиторий для работы с хранилищем пользователей.
    - [log_storage.py](src%2Frepositories%2Flog_storage.py) : Репозиторий для работы с хранилищем логов.
    - [transactions.py](src%2Frepositories%2Ftransactions.py) : Репозиторий для работы транзакциями.
  - `routers/` : Файлы с описанием эндпоинтов.
  - `schemas/` : Схемы данных.
  - `services` : Файлы с сервисами для работы с приложением.

- `tests`: Тесты для проекта.
  - `unit`: Юнит тесты разбиты по файлам в соответствии со структурой проекта.
    - [test_log_storage.py](tests%2Funit%2Frepositories%2Ftest_log_storage.py)
    - [test_user_storage.py](tests%2Funit%2Frepositories%2Ftest_user_storage.py)
    - [test_transactions.py](tests%2Funit%2Frepositories%2Ftest_transactions.py)
    - [test_token_repository.py](tests%2Funit%2Frepositories%2Ftest_token_repository.py)
  - `integration`: Сценарий интеграционных тестов из задания в одном файле + тесты API.
    - [test_main_scenario.py](tests%2Fintegration%2Ftest_main_scenario.py)
    - [test_api_balance.py](tests%2Fintegration%2Ftest_api_balance.py)
    - [test_api_main.py](tests%2Fintegration%2Ftest_api_main.py)
    - [test_api_transactions.py](tests%2Fintegration%2Ftest_api_transactions.py)
    - [test_api_verification.py](tests%2Fintegration%2Ftest_api_verification.py)

- [CHANGELOG.md](CHANGELOG.md) : История изменений проекта.
- `CONTRIBUTING.md` : Рекомендации для контрибьюторов (вы сейчас читаете его).
- [README.md](README.md) : Описание проекта.

## Процесс внесения изменений

1. Создайте форк проекта на GitLab.
2. Клонируйте ваш форк на свой локальный компьютер.
3. Создайте новую ветку для ваших изменений.
4. Внесите необходимые изменения и убедитесь, что все тесты проходят.
5. Отправьте ваши изменения на проверку в виде pull/merge request в основной репозиторий.

## Кодовые стандарты и соглашения

Мы следуем стандартам кодирования, предложенным `wemake-python-styleguide`, а также проверяем типы с помощью `mypy`. Убедитесь, что ваш код соответствует этим требованиям перед отправкой на ревью.

## Процесс ревью

Все изменения в проекте проходят процесс проверки другими разработчиками. Ваш код будет проверен на соответствие стандартам качества и функциональности.

## Полезные ссылки

- [wemake-python-styleguide](https://github.com/wemake-services/wemake-python-styleguide)
- [mypy](http://mypy-lang.org/)
