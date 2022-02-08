import asyncio

from aiokafka import AIOKafkaProducer

from app.settings import settings


producer = AIOKafkaProducer(
    loop=asyncio.get_event_loop(),
    client_id=settings.KAFKA.CLIENT_ID,
    bootstrap_servers=settings.KAFKA.BOOTSTRAP_SERVERS,
    request_timeout_ms=settings.KAFKA.PRODUCER_TIMEOUT_MS,
)
