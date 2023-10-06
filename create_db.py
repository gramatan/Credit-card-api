import asyncio

import asyncpg

from config.config import (
    POSTGRES_DB_NAME,
    POSTGRES_DB_PASS,
    POSTGRES_DB_USER,
    POSTGRES_HOST,
    POSTGRES_PORT,
)


async def create_database():
    conn = await asyncpg.connect(
        user=POSTGRES_DB_USER,
        password=POSTGRES_DB_PASS,
        database='postgres',
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
    )
    try:
        await conn.execute(f'CREATE DATABASE {POSTGRES_DB_NAME}')
    finally:
        await conn.close()

asyncio.run(create_database())
