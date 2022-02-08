from elasticapm.contrib.starlette import ElasticAPM, make_apm_client
from fastapi import FastAPI

from app.settings import settings


def init_apm(app: FastAPI):
    if not settings.APM.ENABLED:
        return

    apm = make_apm_client(
        enabled=settings.APM.ENABLED,
        server_url=settings.APM.SERVER_URL,
        service_name=settings.APM.SERVICE_NAME,
        environment=settings.APM.ENVIRONMENT,
    )
    app.add_middleware(ElasticAPM, client=apm)
