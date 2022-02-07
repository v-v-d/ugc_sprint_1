from pydantic import BaseSettings


class ClickHouse(BaseSettings):
    HOST: str = 'localhost'


class KafkaSettings(BaseSettings):
    TOPIC: str = 'clickhouse'
    HOST: str = 'localhost'
    PORT: int = 9092


class CommonSettings(BaseSettings):
    KAFKA: KafkaSettings = KafkaSettings()
