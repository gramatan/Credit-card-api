"""Скрипты для создания базы."""

create_web_users = """
CREATE TABLE web_users (
    id BIGSERIAL PRIMARY KEY,
    login VARCHAR(100) UNIQUE NOT NULL,
    hashed_password CHAR(60) NOT NULL
);
"""

create_table_cards = """
CREATE TABLE cards (
    id BIGSERIAL PRIMARY KEY,
    card_number VARCHAR(18) UNIQUE NOT NULL,
    card_limit BIGINT NOT NULL CHECK (card_limit >= 0),
    card_info JSONB,
    card_balance BIGINT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);
"""

create_common_logs = """
CREATE TABLE common_logs (
    card_number_id BIGINT,
    datetime_utc TIMESTAMP DEFAULT current_timestamp,
    limit_before BIGINT NOT NULL,
    limit_after BIGINT NOT NULL,
    changes BIGINT NOT NULL,
    PRIMARY KEY (card_number_id, datetime_utc),
    FOREIGN KEY (card_number_id) REFERENCES cards(id) ON DELETE CASCADE
);
"""

create_balance_logs = """
CREATE TABLE balance_logs (
    card_number_id BIGINT,
    datetime_utc TIMESTAMP DEFAULT current_timestamp,
    balance_before BIGINT NOT NULL,
    balance_after BIGINT NOT NULL,
    changes BIGINT NOT NULL,
    PRIMARY KEY (card_number_id, datetime_utc),
    FOREIGN KEY (card_number_id) REFERENCES cards(id) ON DELETE CASCADE
);
"""
