import random
import time
from typing import Generator, Callable, Any

import psycopg2
from clickhouse_driver import Client

from settings import settings


def generate_test_data(chunk_size: int) -> Generator[list[tuple[int, ...]], None, None]:
    chunk = []

    for i in range(settings.ROWS_QTY):
        chunk.append((i, i, i, i))

        if len(chunk) == chunk_size:
            yield chunk
            chunk = []

    yield chunk


def elapsed(test_name: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.monotonic()

            result = func(*args, **kwargs)

            elapsed = time.monotonic() - start_time

            with open("result/stress-testing.txt", "a", encoding="utf-8") as f:
                if "cursor" in kwargs:
                    kwargs.pop("cursor")
                if "client" in kwargs:
                    kwargs.pop("client")
                f.write(
                    f"{test_name} {func.__name__} {kwargs or ''} elapsed {elapsed} \n"
                )

            return result

        return wrapper

    return decorator


def run_postgres_stress_test(chunk_size: int) -> None:
    @elapsed("POSTGRESQL")
    def insert_data(cursor, chunk_size: int) -> None:
        counter = 0
        for chunk in generate_test_data(chunk_size):
            print(f"/////////////////// chunk {counter} processed ///////////////////")
            cursor.executemany(
                f"""
                INSERT INTO {settings.POSTGRES.TABLE_NAME} (id, ts, movie_id, user_id) 
                VALUES (%s, %s, %s, %s)
                """,
                chunk,
            )
            counter += chunk_size

    @elapsed("POSTGRESQL")
    def select_data(cursor) -> None:
        for i in range(settings.SELECTS_QTY):
            print(f"+++++++++++++++++++++++ select {i} +++++++++++++++++++++++")
            random_id = random.randint(1, settings.ROWS_QTY)
            cursor.execute(
                f"SELECT * FROM {settings.POSTGRES.TABLE_NAME} WHERE id={random_id};"
            )

    with psycopg2.connect(settings.POSTGRES.DSN) as pg_conn:
        cursor = pg_conn.cursor()
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {settings.POSTGRES.TABLE_NAME} (
                id INT,
                ts INT,
                movie_id INT,
                user_id INT
            );
            """
        )

        insert_data(cursor=cursor, chunk_size=chunk_size)

        cursor.execute(f"TRUNCATE TABLE {settings.POSTGRES.TABLE_NAME}")

        insert_data(cursor=cursor, chunk_size=1)

        select_data(cursor=cursor)


def run_clickhouse_stress_test(chunk_size: int) -> None:
    @elapsed("CLICK_HOUSE")
    def insert_data(client: Client, chunk_size: int) -> None:
        counter = 0
        for chunk in generate_test_data(chunk_size):
            print(f"/////////////////// chunk {counter} processed ///////////////////")
            client.execute(
                f"INSERT INTO {settings.CLICKHOUSE.DB_NAME}.{settings.CLICKHOUSE.TABLE_NAME} (id, ts, movie_id, user_id) VALUES",
                chunk,
            )
            counter += chunk_size

    @elapsed("CLICK_HOUSE")
    def select_data(client: Client) -> None:
        for i in range(settings.SELECTS_QTY):
            print(f"+++++++++++++++++++++++ select {i} +++++++++++++++++++++++")
            random_id = random.randint(1, settings.ROWS_QTY)
            client.execute(
                f"SELECT * FROM {settings.CLICKHOUSE.DB_NAME}.{settings.CLICKHOUSE.TABLE_NAME} WHERE (id == {random_id})"
            )

    client = Client(settings.CLICKHOUSE.HOST)
    client.execute(
        f"CREATE DATABASE IF NOT EXISTS {settings.CLICKHOUSE.DB_NAME} ON CLUSTER {settings.CLICKHOUSE.CLUSTER_NAME}"
    )
    client.execute(
        f"CREATE TABLE IF NOT EXISTS {settings.CLICKHOUSE.DB_NAME}.{settings.CLICKHOUSE.TABLE_NAME} ON CLUSTER {settings.CLICKHOUSE.CLUSTER_NAME} "
        "(id Int64, ts Int32, movie_id Int64, user_id Int64)"
        " Engine=MergeTree() ORDER BY id"
    )

    insert_data(client=client, chunk_size=chunk_size)

    client.execute(
        f"TRUNCATE TABLE {settings.CLICKHOUSE.DB_NAME}.{settings.CLICKHOUSE.TABLE_NAME} ON CLUSTER {settings.CLICKHOUSE.CLUSTER_NAME}"
    )

    insert_data(client=client, chunk_size=1)

    select_data(client=client)


if __name__ == "__main__":
    # run_postgres_stress_test(settings.CHUNK_SIZE)
    run_clickhouse_stress_test(settings.CHUNK_SIZE)
