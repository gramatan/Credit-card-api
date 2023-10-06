from sqlalchemy import create_engine

from config.config import (
    POSTGRES_DB_NAME,
    POSTGRES_DB_PASS,
    POSTGRES_DB_USER,
    POSTGRES_HOST,
    POSTGRES_PORT,
)

postgres_table_uri = f'postgresql://{POSTGRES_DB_USER}:{POSTGRES_DB_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/postgres'

engine = create_engine(postgres_table_uri, echo=True)
connection = engine.connect()
connection.execute(f'CREATE DATABASE {POSTGRES_DB_NAME}')
connection.close()
