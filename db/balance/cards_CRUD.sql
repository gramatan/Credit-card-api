
-- добавление карты
INSERT INTO cards (card_number, card_limit, card_info, card_balance)
VALUES ('4444555533337777', 0, '{"type": "Visa", "name": "Viktor"}', 0);

-- получаем все карты
SELECT * FROM cards;

-- получаем карту по номеру
SELECT * FROM cards
WHERE card_number = '4444555533337777';

-- обновляем лимит карты
UPDATE cards
SET card_limit = 10000000
WHERE card_number = '4444555533337777';

-- обновляем инфо и баланс
UPDATE cards
SET
    card_info = '{"type": "Visa", "name": "not_Viktor", "age": 20}',
    card_balance = 666
WHERE card_number = '4444555533337777';

-- удаляем карту. запрос то я напишу, но смысл флага is_active в том, что мы не удаляем запись из таблицы, а просто помечаем ее как неактивную
DELETE FROM cards
WHERE card_number = '4444555533337777';

-- Вместо запроса выше используем флаг is_active
UPDATE cards
SET is_active = false
WHERE card_number = '4444555533337777';
