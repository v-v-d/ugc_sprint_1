from logging import getLogger

import elasticapm
import orjson
from aiokafka import AIOKafkaProducer
from kafka.errors import KafkaError
from pydantic import UUID4

from app.api.v1.schemas import FilmProgressInputSchema
from app.kafka import producer
from app.settings import settings

logger = getLogger(__name__)


class ProgressService:
    TOPIC: str = settings.KAFKA.TOPIC

    def __init__(self) -> None:
        self.kafka_producer: AIOKafkaProducer = producer

    @elasticapm.async_capture_span()
    async def send_to_topic(
        self,
        film_id: UUID4,
        progress: FilmProgressInputSchema,
    ) -> None:
        serialized_data = orjson.dumps({"film_id": film_id, **progress.dict()})

        try:
            await self.kafka_producer.send(self.TOPIC, serialized_data)
        except KafkaError:
            logger.exception(
                "Failed to send data to kafka topic %s. Data: %s",
                self.TOPIC,
                serialized_data,
            )
            return

        logger.debug(
            "Successfully sent data to kafka topic %s. Data: %s",
            self.TOPIC,
            serialized_data,
        )


def get_progress_service() -> ProgressService:
    return ProgressService()
