import asyncio
from typing import Any

import orjson
from aiokafka import AIOKafkaConsumer

from app.settings import settings


def deserializer(serialized: bytes) -> dict[str, Any]:
    return orjson.loads(serialized)


def get_consumer() -> AIOKafkaConsumer:
    return AIOKafkaConsumer(
        settings.KAFKA.TOPIC,
        loop=asyncio.get_event_loop(),
        bootstrap_servers=settings.KAFKA.BOOTSTRAP_SERVERS,
        group_id=settings.KAFKA.CONSUMER_GROUP_ID,
        enable_auto_commit=False,
        value_deserializer=deserializer,
    )
