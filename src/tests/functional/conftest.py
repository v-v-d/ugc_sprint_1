import asyncio

import pytest
from async_asgi_testclient import TestClient
from pytest_mock import MockerFixture

from app import kafka, services
from app.main import app
from app.settings import settings


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def disable_apm(session_mocker: MockerFixture) -> None:
    session_mocker.patch.object(settings.APM, "ENABLED", False)


@pytest.fixture(scope="session", autouse=True)
def mocked_kafka(event_loop, session_mocker: MockerFixture) -> None:
    session_mocker.patch.object(kafka, "producer", autospec=True)
    session_mocker.patch.object(services.progress, "producer", autospec=True)


@pytest.fixture(scope="session")
async def client(event_loop) -> TestClient:
    async with TestClient(app) as client:
        client.headers = {"Host": "0.0.0.0", "Content-Type": "application/json"}
        yield client
