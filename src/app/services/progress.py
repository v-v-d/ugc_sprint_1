from logging import getLogger

import backoff
import elasticapm
import orjson
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from kafka.errors import KafkaError, RequestTimedOutError
from pydantic import UUID4

from app.api.v1.schemas import FilmProgressInputSchema
from app.kafka import producer, consumer
from app.settings import settings

logger = getLogger(__name__)


class ProgressServiceError(Exception):
    pass


class SendingToKafkaError(ProgressServiceError):
    pass


class ProgressService:
    TOPIC: str = settings.KAFKA.TOPIC

    def __init__(self) -> None:
        self.kafka_producer: AIOKafkaProducer = producer
        self.kafka_consumer: AIOKafkaConsumer = consumer

    @elasticapm.async_capture_span()
    @backoff.on_exception(
        backoff.expo,
        max_time=settings.BACKOFF.MAX_TIME_SEC,
        exception=SendingToKafkaError,
    )
    async def send_to_topic(
        self,
        film_id: UUID4,
        progress: FilmProgressInputSchema,
    ) -> None:
        serialized_data = orjson.dumps({"film_id": film_id, **progress.dict()})

        try:
            await self.kafka_producer.send(self.TOPIC, serialized_data)
        except RequestTimedOutError as err:
            raise SendingToKafkaError from err
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

    @elasticapm.async_capture_span()
    async def read_from_topic(self) -> None:
        try:
            async for msg in self.kafka_consumer:
                # TODO: #16 push to ClickHouse
                pass
        except KafkaError:
            logger.exception("Failed to read data from kafka topic %s.", self.TOPIC)
            return

        logger.debug("Successfully read data from kafka topic %s.", self.TOPIC)


def get_progress_service() -> ProgressService:
    return ProgressService()
