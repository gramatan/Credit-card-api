"""Продюссеры и консьюмеры для работы с кафкой."""
import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from kafka.errors import KafkaConnectionError

from config.config import KAFKA_HOST, KAFKA_PORT


async def start_producer():
    """
    Запуск продюссера для отправки сообщений в кафку.

    Returns:
        AIOKafkaProducer: Продюссер.
    """
    try:    # noqa: WPS229
        producer = AIOKafkaProducer(
            bootstrap_servers=f'{KAFKA_HOST}:{KAFKA_PORT}',
        )
        await producer.start()
        return producer
    except KafkaConnectionError:
        logging.warning(
            'Kafka server is not available. Verification will not work.',
        )


async def stop_producer(producer):
    """
    Остановка продюссера.

    Args:
        producer: Продюссер.
    """
    if producer:
        await producer.stop()


async def start_consumer():
    """
    Запуск консьюмера для получения сообщений из кафки.

    Returns:
        AIOKafkaConsumer: Консьюмер.
    """
    try:    # noqa: WPS229
        consumer = AIOKafkaConsumer(
            'gran_verify',
            bootstrap_servers=f'{KAFKA_HOST}:{KAFKA_PORT}',
        )
        await consumer.start()
        return consumer
    except KafkaConnectionError:
        logging.warning(
            'Kafka server is not available. Verification will not work.',
        )


async def stop_consumer(consumer):
    """
    Остановка консьюмера.

    Args:
        consumer: Консьюмер.
    """
    if consumer:
        await consumer.stop()


async def kafka_response_listener(app):
    """
    Слушатель ответов от сервиса верификации.

    Args:
        app (FastAPI): Экземпляр приложения.
    """
    consumer = AIOKafkaConsumer(
        'gran_verify_response',
        bootstrap_servers=f'{KAFKA_HOST}:{KAFKA_PORT}',
    )
    await consumer.start()
    try:
        async for message in consumer:
            message_data = json.loads(message.value)
            request_id = message_data['request_id']
            queue = app.state.pending_requests.get(request_id)  # noqa: S113
            if queue:
                await queue.put(message_data['response'])
                app.state.pending_requests.pop(request_id, None)
    except asyncio.CancelledError:
        logging.warning('Kafka consumer was cancelled.')
    finally:
        await consumer.stop()
