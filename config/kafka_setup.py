from aiokafka import AIOKafkaProducer
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
