from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer

from app.security import (
    TokenData,
    decode_jwt_token,
    verify_basic_auth_credentials,
    NotAuthenticatedError,
)

security = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)) -> None:
    try:
        verify_basic_auth_credentials(credentials)
    except NotAuthenticatedError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"},
        )


async def decode_jwt(token: str = Depends(oauth2_scheme)) -> TokenData:
    try:
        return decode_jwt_token(token)
    except NotAuthenticatedError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
