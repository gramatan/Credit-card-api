DROP TABLE IF EXISTS common_logs;
DROP TABLE IF EXISTS balance_logs;
DROP TABLE IF EXISTS cards;

CREATE TABLE cards (
    id BIGSERIAL PRIMARY KEY,
    card_number VARCHAR(18) UNIQUE NOT NULL,
    card_limit BIGINT NOT NULL CHECK (card_limit >= 0),
    card_balance BIGINT NOT NULL,
    card_first_name VARCHAR(50),
    card_second_name VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE common_logs (
    card_number_id BIGINT,
    datetime_utc TIMESTAMP DEFAULT current_timestamp,
    limit_before BIGINT NOT NULL,
    limit_after BIGINT NOT NULL,
    changes BIGINT NOT NULL,
    PRIMARY KEY (card_number_id, datetime_utc),
    FOREIGN KEY (card_number_id) REFERENCES cards(id) ON DELETE CASCADE
);

CREATE TABLE balance_logs (
    card_number_id BIGINT,
    datetime_utc TIMESTAMP DEFAULT current_timestamp,
    balance_before BIGINT NOT NULL,
    balance_after BIGINT NOT NULL,
    changes BIGINT NOT NULL,
    PRIMARY KEY (card_number_id, datetime_utc),
    FOREIGN KEY (card_number_id) REFERENCES cards(id) ON DELETE CASCADE
);
