from pydantic import BaseSettings


class PostgresSetting(BaseSettings):
    NAME: str = "postgres"
    USER: str = "postgres"
    PASSWORD: str = "postgres"
    HOST: str = "localhost"
    PORT: int = 6432


class Clickhouse(BaseSettings):
    HOST: str = "localhost"


class CommonSettings(BaseSettings):
    POSTGRES: PostgresSetting = PostgresSetting()
    CLICKHOUSE: Clickhouse = Clickhouse()
