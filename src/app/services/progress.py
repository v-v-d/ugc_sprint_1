from datetime import datetime
from logging import getLogger

import backoff
import elasticapm
from aiokafka import AIOKafkaProducer
from kafka.errors import KafkaError, RequestTimedOutError
from pydantic import UUID4

from app.api.v1.schemas import FilmProgressInputSchema
from app.kafka import producer_container
from app.settings import settings

logger = getLogger(__name__)


class ProgressServiceError(Exception):
    pass


class ProgressService:
    TOPIC: str = settings.KAFKA.TOPIC

    def __init__(self) -> None:
        self.kafka_producer: AIOKafkaProducer = producer_container.instance

    @elasticapm.async_capture_span()
    @backoff.on_exception(
        backoff.expo,
        max_time=settings.BACKOFF.MAX_TIME_SEC,
        exception=RequestTimedOutError,
    )
    async def send_to_topic(
        self,
        film_id: UUID4,
        progress: FilmProgressInputSchema,
    ) -> None:
        data = {
            "film_id": film_id,
            **progress.dict(),
            "created_at": datetime.now().timestamp(),
        }

        try:
            await self.kafka_producer.send(self.TOPIC, data)
        except RequestTimedOutError as err:
            # catch it in backoff
            raise err
        except KafkaError:
            logger.exception(
                "Failed to send data to kafka topic %s. Data: %s",
                self.TOPIC,
                data,
            )
            return

        logger.debug(
            "Successfully sent data to kafka topic %s. Data: %s",
            self.TOPIC,
            data,
        )


def get_progress_service() -> ProgressService:
    return ProgressService()
