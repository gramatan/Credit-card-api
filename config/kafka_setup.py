from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from kafka.errors import KafkaConnectionError


async def start_producer():
    try:
        producer = AIOKafkaProducer(bootstrap_servers='localhost:24301')
        await producer.start()
        return producer
    except KafkaConnectionError:
        print('Kafka server is not available. Verification will not work.')


async def stop_producer(producer):
    if producer:
        await producer.stop()


async def start_consumer():
    try:
        consumer = AIOKafkaConsumer(
            'gran_verify',
            bootstrap_servers='localhost:24301',
        )
        await consumer.start()
        return consumer
    except KafkaConnectionError:
        print('Kafka server is not available. Verification consumer will not work.')


async def stop_consumer(consumer):
    if consumer:
        await consumer.stop()
