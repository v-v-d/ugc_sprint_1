import psycopg2
from psycopg2.extras import DictCursor
from common_settings import CommonSettings
from model import Data
from postgres import PostgresStressTest
from dataclasses import astuple
from clickhouse_driver import Client
from clickhouse import ClickHouse


def collect_data():
    data = []
    data_count = 1
    post_id = 1
    user_id = 1
    timestamp = 100
    move_id = 1
    while True:
        data.append(
            Data(id=post_id, user_id=user_id, timestamp=timestamp, move_id=move_id)
        )
        data_count += 1
        post_id += 1
        user_id += 1
        timestamp += 1
        move_id += 1
        if data_count == 10000000:
            break
    return data


if __name__ == "__main__":
    data = collect_data()
    settings = CommonSettings()
    dsl = {
        "dbname": settings.POSTGRES.NAME,
        "user": settings.POSTGRES.USER,
        "password": settings.POSTGRES.PASSWORD,
        "host": settings.POSTGRES.HOST,
        "port": settings.POSTGRES.PORT,
    }

    with psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        postgres_stress_test = PostgresStressTest(pg_conn)
        postgres_stress_test.save_all_data(
            [astuple(obj) for obj in data],
            table=f"cluster_data",
            rows_name=",".join(data[-1].__dataclass_fields__.keys()),
        )
        postgres_stress_test.search_data(table="cluster_data")
    clickhouse = ClickHouse(Client(settings.CLICKHOUSE.HOST))
    clickhouse.save_all_data([astuple(obj) for obj in data])
    clickhouse.search_clickhouse()
