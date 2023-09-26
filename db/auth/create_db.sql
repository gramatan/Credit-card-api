CREATE TABLE web_users (
    id BIGSERIAL PRIMARY KEY,
    login VARCHAR(100) UNIQUE NOT NULL,
    hashed_password CHAR(60) NOT NULL
);
