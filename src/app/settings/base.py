from pathlib import Path

from pydantic import BaseSettings, AnyUrl, validator


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


class ClickHouseSettings(BaseSettings):
    HOST: str
    PORT: str
    PROTOCOL: str = "http"
    TABLE_NAME: str
    URL: AnyUrl = None

    @validator("URL", pre=True)
    def build_url(cls, v, values) -> str:
        if v:
            return v

        return f"{values['PROTOCOL']}://{values['HOST']}:{values['PORT']}/"

    class Config:
        env_prefix = "CH_"


class ETLSettings(BaseSettings):
    CHUNK_SIZE: int = 5
    KAFKA_POLL_TIMEOUT_MS: int = 10000

    class Config:
        env_prefix = "ETL_"


class CommonSettings(BaseSettings):
    PROJECT_NAME: str = "ugc-app"
    OPENAPI_URL: str = "/api/openapi.json"
    DEBUG: bool = False
    TESTING: bool = False
    LOG_LEVEL: str = "INFO"
    SHARED_DIR: str = "/code/shared"
    DIR_LOGS: Path = Path(SHARED_DIR, "/code/shared/logs")

    UVICORN: UvicornSettings = UvicornSettings()
    SECURITY: SecuritySettings = SecuritySettings()
    APM: APMSettings = APMSettings()
    KAFKA: KafkaSettings = KafkaSettings()
    BACKOFF: BackoffSettings = BackoffSettings()
    CH: ClickHouseSettings = ClickHouseSettings()
    ETL: ETLSettings = ETLSettings()
