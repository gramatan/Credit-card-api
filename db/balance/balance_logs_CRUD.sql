
-- создаем лог
INSERT INTO balance_logs (card_number_id, balance_before, balance_after, changes)
VALUES (1, 5000, 4000, -1000);

-- читаем логи
SELECT * FROM balance_logs
WHERE card_number_id = 1 AND
        datetime_utc BETWEEN '1970-01-01 00:00:00' AND '2970-01-01 00:00:00';

-- удаляем логи по номеру карточки
DELETE FROM balance_logs WHERE card_number_id = 1;