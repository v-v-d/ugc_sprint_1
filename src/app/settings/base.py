from pathlib import Path

from pydantic import BaseSettings


class UvicornSettings(BaseSettings):
    app: str = "app.main:app"
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    workers: int = 3

    class Config:
        env_prefix = "UVICORN_"


class SecuritySettings(BaseSettings):
    class JWTAuthSettings(BaseSettings):
        SECRET_KEY: str
        ALGORITHM: str

        class Config:
            env_prefix = "SECURITY_JWT_AUTH_"

    class BasicAuthSettings(BaseSettings):
        USERNAME: str
        PASSWD: str

        class Config:
            env_prefix = "SECURITY_BASIC_AUTH_"

    ALLOWED_HOSTS: list[str]
    JWT_AUTH: JWTAuthSettings = JWTAuthSettings()
    BASIC_AUTH: BasicAuthSettings = BasicAuthSettings()

    class Config:
        env_prefix = "SECURITY_"


class APMSettings(BaseSettings):
    ENABLED: bool
    SERVER_URL: str
    SERVICE_NAME: str
    ENVIRONMENT: str

    class Config:
        env_prefix = "APM_"


class KafkaSettings(BaseSettings):
    CLIENT_ID: str = "ugc-app"
    TOPIC: str
    BOOTSTRAP_SERVERS: str
    PRODUCER_TIMEOUT_MS: int
    CONSUMER_GROUP_ID: str

    class Config:
        env_prefix = "KAFKA_"


class BackoffSettings(BaseSettings):
    MAX_TIME_SEC: int

    class Config:
        env_prefix = "BACKOFF_"


class SentrySettings(BaseSettings):
    DSN: str
    ENVIRONMENT: str
    ENABLED: bool = True
    DEBUG: bool = False
    SAMPLE_RATE: float = 1.0

    class Config:
        env_prefix = 'SENTRY_'


class CommonSettings(BaseSettings):
    PROJECT_NAME: str = "ugc-app"
    OPENAPI_URL: str = "/api/openapi.json"
    DEBUG: bool = False
    TESTING: bool = False
    LOG_LEVEL: str = "INFO"
    SHARED_DIR: str = "/code/shared"
    DIR_LOGS: Path = Path(SHARED_DIR, "logs")

    UVICORN: UvicornSettings = UvicornSettings()
    SECURITY: SecuritySettings = SecuritySettings()
    APM: APMSettings = APMSettings()
    KAFKA: KafkaSettings = KafkaSettings()
    BACKOFF: BackoffSettings = BackoffSettings()
    SENTRY: SentrySettings = SentrySettings()
