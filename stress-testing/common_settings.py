from pydantic import BaseSettings


class ClickHouseSetting(BaseSettings):
    HOST: str = 'localhost'

    class Config:
        env_prefix = "CLICKHOUSE_"


class PostgresSetting(BaseSettings):
    NAME: str = 'postgres'
    USER: str = 'postgres'
    PASSWORD: str = 'postgres'
    HOST: str = 'localhost'
    PORT: int = 6432

    class Config:
        env_prefix = "DB_"


class CommonSettings(BaseSettings):
    CLICKHOUSE: ClickHouseSetting = ClickHouseSetting()
    POSTGRES: PostgresSetting = PostgresSetting()
