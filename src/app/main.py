from logging import config

from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import ORJSONResponse

from app.api import api_root
from app.api.docs import router as api_docs
from app.apm import init_apm
from app.kafka import producer
from app.settings import settings
from app.settings.logging import LOGGING

config.dictConfig(LOGGING)

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    default_response_class=ORJSONResponse,
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.SECURITY.ALLOWED_HOSTS)


@app.on_event("startup")
async def startup():
    await producer.start()


@app.on_event("shutdown")
async def shutdown():
    await producer.stop()


app.include_router(api_docs)
app.include_router(api_root, prefix="/api")

init_apm(app)
