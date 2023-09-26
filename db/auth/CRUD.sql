
-- добавление пользователя. Хэш генерим на стороне приложения, а не в запросе.
INSERT INTO web_users (login, hashed_password)
VALUES ('test_user', 'test_password_hash');

-- получение всех пользователей со всеми полями.
SELECT * FROM web_users;

-- получение конкретного пользователя по имени
SELECT * FROM web_users
WHERE login = 'test_user';

-- и по логину
SELECT * FROM web_users
WHERE id = 1;

-- изменение пароля у пользователя
UPDATE web_users
SET hashed_password = 'new_pass_hash'
WHERE id = 1;

-- Удаление пользователя по ID
DELETE FROM web_users
WHERE id = 1;
