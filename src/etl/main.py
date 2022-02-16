from logging import getLogger
from typing import AsyncGenerator, Optional

from aiochclient import ChClient, ChClientError
from aiokafka import AIOKafkaConsumer, ConsumerRecord
from httpx import AsyncClient

from etl.kafka import get_consumer
from etl.settings import settings

logger = getLogger(__name__)


class ClickHouseConnectionError(Exception):
    pass


class ETL:
    CHUNK_SIZE: int = settings.ETL.CHUNK_SIZE
    POLL_TIMEOUT: int = settings.ETL.KAFKA_POLL_TIMEOUT_MS
    CH_URL: str = settings.CH.URL
    CH_TABLE: str = settings.CH.TABLE_NAME

    def __init__(self) -> None:
        self.kafka_consumer: AIOKafkaConsumer = get_consumer()
        self.ch_client: Optional[ChClient] = None

    async def run(self) -> None:
        async with AsyncClient() as session:
            self.ch_client = ChClient(session=session, url=self.CH_URL)

            if not await self.ch_client.is_alive():
                raise ClickHouseConnectionError

            await self.init_storage()

            async for chunk in self.extract_by_chunks():
                await self.load(chunk)

    async def init_storage(self) -> None:
        await self.ch_client.execute(
            f"CREATE DATABASE IF NOT EXISTS movies ON CLUSTER company_cluster"
        )
        await self.ch_client.execute(
            f"""
            CREATE TABLE IF NOT EXISTS movies.{self.CH_TABLE} 
            ON CLUSTER company_cluster 
            (film_id String, user_id String, progress Int16, total Int16, created_at Int32) 
            Engine=MergeTree() 
            ORDER BY created_at
            """
        )

    async def extract_by_chunks(self) -> AsyncGenerator[list[ConsumerRecord], None]:
        """
        Connect to Kafka topic and consume it by chunks with specified size.
        Wait until the CHUNK_SIZE has been reached or until the POLL_TIMEOUT expires
        and yield it.
        """
        async with self.kafka_consumer:
            chunk = []

            while True:
                result = await self.kafka_consumer.getmany(timeout_ms=self.POLL_TIMEOUT)

                if not result and chunk:
                    yield chunk
                    chunk = []

                chunk.extend(*result.values())

                if len(chunk) == self.CHUNK_SIZE:
                    yield chunk
                    chunk = []

    async def load(self, chunk: list[ConsumerRecord]) -> None:
        data = [tuple(msg.value.values()) for msg in chunk]

        try:
            await self.ch_client.execute(
                f"INSERT INTO movies.{self.CH_TABLE} (film_id, user_id, progress, total, created_at) VALUES",
                *data,
            )
        except ChClientError:
            logger.exception("Failed to load data to ClickHouse!")
            return

        await self.kafka_consumer.commit()
        logger.debug("Successfully load data to ClickHouse!")


async def start_etl() -> None:
    etl = ETL()
    await etl.run()
