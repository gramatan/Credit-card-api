"""Основной файл приложения."""
import asyncio
import json

from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI
from pydantic_settings import BaseSettings

from config.config import AUTH_APP_HOST, AUTH_APP_PORT, PATH_PREFIX
from config.kafka_setup import start_producer, stop_producer
from credit_card_auth.src.routers import (
    balance_router,
    token_router,
    transactions_router,
    verification_router,
)


class Settings(BaseSettings):
    """Конфигурация приложения."""

    app_host: str = AUTH_APP_HOST
    app_port: int = AUTH_APP_PORT


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    app.state.kafka_producer = await start_producer()
    app.state.pending_requests = {}
    asyncio.create_task(kafka_response_listener())


@app.on_event("shutdown")
async def shutdown_event():
    await stop_producer(app.state.kafka_producer)


app.include_router(token_router.router, prefix=PATH_PREFIX, tags=['auth'])
app.include_router(balance_router.router, prefix=PATH_PREFIX, tags=['balance'])
app.include_router(
    verification_router.router,
    prefix=PATH_PREFIX,
    tags=['verification'],
)
app.include_router(
    transactions_router.router,
    prefix=PATH_PREFIX,
    tags=['transactions'],
)


async def kafka_response_listener():
    consumer = AIOKafkaConsumer(
        "gran_verify_response",
        bootstrap_servers='localhost:24301',
    )
    await consumer.start()
    try:
        async for message in consumer:
            data = json.loads(message.value)
            request_id = data["request_id"]
            queue = app.state.pending_requests.get(request_id)
            if queue:
                await queue.put(data["response"])
                del app.state.pending_requests[request_id]
    finally:
        await consumer.stop()


if __name__ == '__main__':
    import uvicorn  # noqa: WPS433
    settings = Settings()
    uvicorn.run(
        app,
        host=settings.app_host,
        port=settings.app_port,
        ssl_keyfile='localhost.key',
        ssl_certfile='localhost.crt',
    )
