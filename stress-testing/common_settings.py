from pydantic import BaseSettings


class PostgresSetting(BaseSettings):
    NAME: str = "postgres"
    USER: str = "postgres"
    PASSWORD: str = "postgres"
    HOST: str = "localhost"
    PORT: int = 6432

    class Config:
        env_prefix = "DB_"


class CommonSettings(BaseSettings):
    POSTGRES: PostgresSetting = PostgresSetting()
