
-- добавление карты
INSERT INTO cards (card_number, card_limit, card_first_name, card_second_name, card_balance)
VALUES ('4444555533337777', 0, 'name', 'surname', 0);

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
    card_first_name = 'Vasiliy',
    card_balance = 666
WHERE card_number = '4444555533337777';

-- удаляем карту. Вместо запроса ниже используем флаг is_active
DELETE FROM cards
WHERE card_number = '4444555533337777';

-- Вместо запроса выше используем флаг is_active
UPDATE cards
SET is_active = false
WHERE card_number = '4444555533337777';
