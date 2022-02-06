from fastapi import APIRouter, Depends, status

from app.api import v1
from app.api.dependencies.auth import decode_jwt
from app.api.schemas import ErrorSchema

api_root = APIRouter(
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorSchema},
    },
    dependencies=[Depends(decode_jwt)],
)

api_root.include_router(v1.progresses.router, prefix="/v1/progresses", tags=["v1 progresses"])
