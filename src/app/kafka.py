import asyncio
from typing import Optional, Any

import orjson
from aiokafka import AIOKafkaProducer

from app.settings import settings


def serializer(value: dict[str, Any]) -> bytes:
    return orjson.dumps(value)


class KafkaProducerContainer:
    _instance: Optional[AIOKafkaProducer] = None

    @property
    def instance(self) -> AIOKafkaProducer:
        if not self._instance:
            self._instance = AIOKafkaProducer(
                loop=asyncio.get_event_loop(),
                client_id=settings.KAFKA.CLIENT_ID,
                bootstrap_servers=settings.KAFKA.BOOTSTRAP_SERVERS,
                request_timeout_ms=settings.KAFKA.PRODUCER_TIMEOUT_MS,
                value_serializer=serializer,
            )
        return self._instance


producer_container = KafkaProducerContainer()
