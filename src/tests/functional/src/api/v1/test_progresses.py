from typing import Any
from uuid import UUID

import pytest
from fastapi import status
from mimesis.locales import Locale
from mimesis.schema import Field
from pytest_mock import MockerFixture

from app.api.schemas import DefaultSuccessResponse
from app.main import app
from app.services import progress

fake = Field(locale=Locale.RU)

pytestmark = pytest.mark.asyncio


@pytest.fixture(autouse=True)
def mocked_progress_service(mocker: MockerFixture) -> None:
    mock = mocker.AsyncMock(spec=progress.ProgressService)
    mocker.patch.object(progress, "get_progress_service", return_value=mock)


@pytest.fixture
def film_id() -> UUID:
    return fake("uuid_object")


@pytest.fixture
def request_body() -> dict[str, Any]:
    total = fake("integer_number", start=3600, end=7200)
    progress = fake("integer_number", start=0, end=total)

    return dict(
        user_id=fake("uuid"),
        progress=progress,
        total=total,
        timestamp_local=fake("integer_number", start=1644179333, end=1644179433),
    )


async def test_ok(client, film_id, request_body):
    response = await client.post(
        path=app.url_path_for("send_film_progress", film_id=str(film_id)),
        json=request_body,
    )
    assert response.status_code == status.HTTP_202_ACCEPTED, response.json()
    assert response.json() == DefaultSuccessResponse()


@pytest.mark.origin_jwt_decode
async def test_unauthorized_no_jwt(client, film_id, request_body):
    response = await client.post(
        path=app.url_path_for("send_film_progress", film_id=str(film_id)),
        json=request_body,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.json()


@pytest.mark.origin_jwt_decode
async def test_unauthorized_invalid_jwt(
    client, film_id, request_body, invalid_jwt_token
):
    response = await client.post(
        path=app.url_path_for("send_film_progress", film_id=str(film_id)),
        json=request_body,
        headers={
            "Authorization": invalid_jwt_token,
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.json()


@pytest.mark.origin_jwt_decode
async def test_unauthorized_invalid_jwt_payload(
    client, film_id, request_body, jwt_with_invalid_payload
):
    response = await client.post(
        path=app.url_path_for("send_film_progress", film_id=str(film_id)),
        json=request_body,
        headers={
            "Authorization": jwt_with_invalid_payload,
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.json()
    assert False
