from pydantic import BaseSettings, validator, PostgresDsn


class PostgresSettings(BaseSettings):
    USER: str = "postgres"
    PASSWORD: str = "passwd"
    HOST: str = "pg"
    PORT: int = 5432
    PATH: str = "stress-test-db"
    DSN: PostgresDsn = None
    TABLE_NAME: str = "stress-test"

    @validator("DSN", pre=True)
    def build_dsn(cls, v, values) -> str:
        if v:
            return v

        user = values["USER"]
        passwd = values["PASSWORD"]
        host = values["HOST"]
        port = values["PORT"]
        path = values["PATH"]

        return f"postgres://{user}:{passwd}@{host}:{port}/{path}"


class ClickhouseSettings(BaseSettings):
    HOST: str = "localhost"


class Settings(BaseSettings):
    POSTGRES: PostgresSettings = PostgresSettings()
    CLICKHOUSE: ClickhouseSettings = ClickhouseSettings()
    ROWS_QTY: int = 10000000
    CHUNK_SIZE: int = 1000
    SELECTS_QTY: int = 100


settings = Settings()
