CREATE TABLE cards (
    id BIGSERIAL PRIMARY KEY,
    card_number VARCHAR(18) UNIQUE NOT NULL,
    card_limit BIGINT NOT NULL CHECK (card_limit >= 0),
    card_info JSONB,
    card_balance BIGINT NOT NULL,
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
