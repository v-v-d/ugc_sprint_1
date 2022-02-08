import pytest
from fastapi import status
from fastapi.security import HTTPBasicCredentials
from pytest_mock import MockerFixture

from app.api.dependencies import auth
from app.main import app
from app.settings import settings

TARGET_PATHS = (
    app.url_path_for("get_swagger"),
    app.url_path_for("get_redoc"),
    app.url_path_for("get_openapi_json"),
)
pytestmark = [pytest.mark.asyncio, pytest.mark.parametrize("url_path", TARGET_PATHS)]


@pytest.fixture
def valid_basic_auth(mocker: MockerFixture) -> None:
    auth_obj = HTTPBasicCredentials(
        username=settings.SECURITY.BASIC_AUTH.USERNAME,
        password=settings.SECURITY.BASIC_AUTH.PASSWD,
    )

    dependency_overrides = {auth.security: lambda: auth_obj}
    mocker.patch.object(app, "dependency_overrides", dependency_overrides)


@pytest.fixture
def invalid_basic_auth(mocker: MockerFixture) -> None:
    auth_obj = HTTPBasicCredentials(
        username="invalid username",
        password="invalid password",
    )

    dependency_overrides = {auth.security: lambda: auth_obj}
    mocker.patch.object(app, "dependency_overrides", dependency_overrides)


async def test_ok(client, url_path, valid_basic_auth):
    response = await client.get(path=url_path)
    assert response.status_code == status.HTTP_200_OK, response.json()


async def test_unauthorized(client, url_path, invalid_basic_auth):
    response = await client.get(path=url_path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.json()
