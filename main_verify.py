"""Основной файл приложения."""
import asyncio
import json
from concurrent.futures import ProcessPoolExecutor

from fastapi import FastAPI
from pydantic_settings import BaseSettings

from config.config import VERIFICATION_HOST, VERIFICATION_PORT
from config.kafka_setup import stop_consumer, start_consumer, start_producer, stop_producer
from credit_card_verify.src.routers import verify_router


class Settings(BaseSettings):
    """Конфигурация приложения."""

    app_host: str = VERIFICATION_HOST
    app_port: int = VERIFICATION_PORT


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    app.state.kafka_producer = await start_producer()
    app.state.kafka_consumer = await start_consumer()
    asyncio.create_task(kafka_listener(app))


@app.on_event("shutdown")
async def shutdown_event():
    await stop_consumer(app.state.kafka_consumer)
    await stop_producer(app.state.kafka_producer)

executor = ProcessPoolExecutor(max_workers=1)

app.include_router(verify_router.router, prefix='/api', tags=['verify'])


async def kafka_listener(app: FastAPI):
    from credit_card_verify.src.services.verify_service import VerifyService
    consumer = app.state.kafka_consumer
    producer = app.state.kafka_producer
    async for message in consumer:
        message_data = json.loads(message.value.decode('utf-8'))

        request_id = message_data["request_id"]
        selfie_path = message_data["selfie_path"]
        document_path = message_data["document_path"]

        verification_service = VerifyService()
        result = await verification_service.verify(selfie_path, document_path)

        print(result)
        response_data = {
            "request_id": request_id,
            "response": str(result)
        }
        message_data_bytes = json.dumps(response_data).encode('utf-8')
        await producer.send("gran_verify_response", value=message_data_bytes)


if __name__ == '__main__':
    import uvicorn  # noqa: WPS433
    settings = Settings()
    uvicorn.run(
        app,
        host=settings.app_host,
        port=settings.app_port,
    )
