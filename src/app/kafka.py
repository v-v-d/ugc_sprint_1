import asyncio

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from app.settings import settings

loop = asyncio.get_event_loop()


producer = AIOKafkaProducer(
    loop=loop,
    client_id=settings.KAFKA.CLIENT_ID,
    bootstrap_servers=settings.KAFKA.BOOTSTRAP_SERVERS,
    request_timeout_ms=settings.KAFKA.PRODUCER_TIMEOUT_MS,
)

consumer = AIOKafkaConsumer(
    settings.KAFKA.TOPIC,
    loop=loop,
    bootstrap_servers=settings.KAFKA.BOOTSTRAP_SERVERS,
    group_id=settings.KAFKA.CONSUMER_GROUP_ID,
)
