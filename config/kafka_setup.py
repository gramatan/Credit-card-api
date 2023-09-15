"""Продюссеры и консьюмеры для работы с кафкой."""
import logging

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from kafka.errors import KafkaConnectionError


async def start_producer():
    """
    Запуск продюссера для отправки сообщений в кафку.

    Returns:
        AIOKafkaProducer: Продюссер.
    """
    try:    # noqa: WPS229
        producer = AIOKafkaProducer(bootstrap_servers='localhost:24301')
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
            bootstrap_servers='localhost:24301',
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
