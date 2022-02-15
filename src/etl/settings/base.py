from pathlib import Path

from pydantic import BaseSettings, AnyUrl, validator


class KafkaSettings(BaseSettings):
    CLIENT_ID: str = "ugc-app"
    TOPIC: str
    BOOTSTRAP_SERVERS: str
    PRODUCER_TIMEOUT_MS: int
    CONSUMER_GROUP_ID: str

    class Config:
        env_prefix = "KAFKA_"


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
    PROJECT_NAME: str = "ugc-etl"
    DEBUG: bool = False
    TESTING: bool = False
    LOG_LEVEL: str = "INFO"
    SHARED_DIR: str = "/code/shared"
    DIR_LOGS: Path = Path(SHARED_DIR, "/code/shared/logs")

    KAFKA: KafkaSettings = KafkaSettings()
    CH: ClickHouseSettings = ClickHouseSettings()
    ETL: ETLSettings = ETLSettings()
