from pydantic import BaseSettings, validator, PostgresDsn


class PostgresSettings(BaseSettings):
    USER: str = "postgres"
    PASSWORD: str = "passwd"
    HOST: str = "pg"
    PORT: int = 5432
    DB_PATH: str = "postgres"
    DSN: PostgresDsn = None
    TABLE_NAME: str = "stress_test"

    @validator("DSN", pre=True)
    def build_dsn(cls, v, values) -> str:
        if v:
            return v

        user = values["USER"]
        passwd = values["PASSWORD"]
        host = values["HOST"]
        port = values["PORT"]
        path = values["DB_PATH"]

        return f"postgres://{user}:{passwd}@{host}:{port}/{path}"


class ClickhouseSettings(BaseSettings):
    HOST: str = "clickhouse-node1-st"
    DB_NAME: str = "example"
    CLUSTER_NAME: str = "company_cluster"
    TABLE_NAME: str = "regular_table"


class Settings(BaseSettings):
    POSTGRES: PostgresSettings = PostgresSettings()
    CLICKHOUSE: ClickhouseSettings = ClickhouseSettings()
    ROWS_QTY: int = 10000000
    CHUNK_SIZE: int = 1000
    SELECTS_QTY: int = 100


settings = Settings()
