
import pytest
from datetime import datetime, timedelta

from src.repositories.log_storage import LogStorage


@pytest.mark.parametrize('card_id, from_date, to_date, expected_length', [
    pytest.param(
        '1234567890',
        datetime(year=2024, month=2, day=29),
        datetime(year=2024, month=2, day=29),
        1,
        id='One day',
    ),
    pytest.param(
        '1234567890',
        datetime(year=2023, month=8, day=31),
        datetime(year=2024, month=2, day=24),
        0,
        id='Before start of logs',
    ),
    pytest.param(
        '1234567890',
        datetime(year=2024, month=3, day=6),
        datetime(year=2024, month=3, day=28),
        0,
        id='After end of logs',
    ),
    pytest.param(
        '1234567890',
        datetime(year=2024, month=2, day=26),
        datetime(year=2024, month=2, day=28),
        3,
        id='Part of logs'),
    pytest.param(
        '1234567890',
        datetime(year=2024, month=2, day=25),
        datetime(year=2024, month=3, day=5),
        10,
        id='All logs'),
    pytest.param(
        '3453',
        datetime(year=2024, month=2, day=26),
        datetime(year=2024, month=2, day=28),
        0,
        id='No logs'),
])
def test_get_balance_history(card_id, from_date, to_date, expected_length, log_storage_with_history):
    history = log_storage_with_history.get_balance_history(card_id, from_date, to_date)
    assert len(history) == expected_length


@pytest.mark.parametrize('log_type, logs_count, expected_length', [
    ('balance_logs', 3, 3),
    ('balance_logs', 5, 5),
    ('common_logs', 2, 2),
    ('common_logs', 3, 3)
])
def test_save_logs(logs_collection, log_type, logs_count, expected_length):
    storage = LogStorage()
    for log in logs_collection[log_type][:logs_count]:
        storage.save(log)

    if log_type == 'balance_logs':
        assert len(storage._balance_logs['1234567890']) == expected_length
    else:
        assert len(storage._other_logs) == expected_length
