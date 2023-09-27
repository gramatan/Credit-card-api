
-- создаем лог
INSERT INTO common_logs (card_number_id, limit_before, limit_after, changes)
VALUES (1, 5000, 4000, -1000);

-- читаем логи
SELECT * FROM common_logs
WHERE card_number_id = 1 AND
        datetime_utc BETWEEN '1970-01-01 00:00:00' AND '2970-01-01 00:00:00';

-- читаем все логи(нетипичное использование)
select * from common_logs;

-- обвноление логов(нетипичное использование)
UPDATE balance_logs
SET balance_before = 100000, balance_after = 200000, changes = 100000
WHERE card_number_id = 4 AND
        datetime_utc = '2023-09-26 09:16:00.625240';

-- удаляем логи по номеру карточки(нетипичное использование)
DELETE FROM common_logs WHERE card_number_id = 1;
