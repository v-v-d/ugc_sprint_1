from uuid import UUID

import pytest
from aiokafka import AIOKafkaProducer
from kafka.errors import KafkaError
from mimesis.locales import Locale
from mimesis.schema import Field
from pytest_mock import MockerFixture

from app.api.v1.schemas import FilmProgressInputSchema
from app.services import progress

fake = Field(locale=Locale.RU)

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mocked_kafka_producer(mocker: MockerFixture) -> None:
    mock = mocker.AsyncMock(spec=AIOKafkaProducer)
    mocker.patch.object(progress.producer_container, "_instance", return_value=mock)


@pytest.fixture
def failed_kafka_producer(mocker: MockerFixture) -> None:
    mock = mocker.AsyncMock(spec=AIOKafkaProducer)
    mock.send.side_effect = KafkaError
    mocker.patch.object(progress.producer_container, "_instance", return_value=mock)


@pytest.fixture
def service_obj(mocked_kafka_producer) -> progress.ProgressService:
    return progress.get_progress_service()


@pytest.fixture
def failed_service_obj(failed_kafka_producer) -> progress.ProgressService:
    return progress.get_progress_service()


@pytest.fixture
def data() -> tuple[UUID, FilmProgressInputSchema]:
    film_id = fake("uuid_object")
    schema = FilmProgressInputSchema(
        user_id=fake("uuid_object"),
        progress=fake("integer_number", start=0, end=3600),
        total=fake("integer_number", start=3600, end=7200),
        timestamp_local=fake("integer_number", start=1644179333, end=1644179433),
    )
    return film_id, schema


async def test_send_to_topic_ok(service_obj, data):
    result = await service_obj.send_to_topic(*data)

    service_obj.kafka_producer.send.assert_called_once()
    assert result is None


async def test_send_to_topic_failed(failed_service_obj, data):
    result = await failed_service_obj.send_to_topic(*data)

    failed_service_obj.kafka_producer.send.assert_called_once()
    assert result is None
