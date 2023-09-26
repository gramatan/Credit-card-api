
-- создаем лог
INSERT INTO balance_logs (card_number_id, balance_before, balance_after, changes)
VALUES (1, 5000, 4000, -1000);

-- читаем логи
SELECT * FROM balance_logs
WHERE card_number_id = 1 AND
        datetime_utc BETWEEN '1970-01-01 00:00:00' AND '2970-01-01 00:00:00';

-- читаем все логи(нетипичное использование)
select * from balance_logs;

-- обновляем лог(нетипичное использование)
UPDATE balance_logs
SET balance_before = 100000, balance_after = 200000, changes = 100000
WHERE card_number_id = 4 AND
        datetime_utc = '2023-09-26 09:16:00.625240';

-- удаляем логи по номеру карточки
DELETE FROM balance_logs WHERE card_number_id = 1;