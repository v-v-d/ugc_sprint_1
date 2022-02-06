import pytest
from app.api.dependencies.auth import oauth2_scheme
from jose import jwt
from pytest_mock import MockerFixture

from app.main import app
from app.settings import settings


@pytest.fixture
def jwt_with_invalid_payload():
    payload = {}
    token = jwt.encode(
        payload,
        settings.SECURITY.JWT_AUTH.SECRET_KEY,
        algorithm=settings.SECURITY.JWT_AUTH.ALGORITHM,
    )
    return f"Bearer {token}"


@pytest.fixture
def invalid_jwt_token() -> str:
    return "Bearer xxx.xxx.xxx"


@pytest.fixture
def valid_jwt_token():
    payload = {
        "is_admin": False,
        "roles": [],
    }
    return jwt.encode(
        payload,
        settings.SECURITY.JWT_AUTH.SECRET_KEY,
        algorithm=settings.SECURITY.JWT_AUTH.ALGORITHM,
    )


@pytest.fixture(autouse=True)
def mocked_jwt_decode(request, mocker: MockerFixture, valid_jwt_token) -> None:
    if "origin_jwt_decode" in request.keywords:
        return
    
    dependency_overrides = {oauth2_scheme: lambda: valid_jwt_token}
    mocker.patch.object(app, "dependency_overrides", dependency_overrides)
