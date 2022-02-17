import random
import time
from typing import Generator, Callable, Any

import psycopg2
from clickhouse_driver import Client

from settings import settings


def generate_test_data(chunk_size: int) -> Generator[list[tuple[int, ...]], None]:
    chunk = []

    for i in range(settings.ROWS_QTY):
        chunk.append((i, i, i, i))

        if len(chunk) == chunk_size:
            yield chunk
            chunk = []

    yield chunk


def elapsed(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        elapsed = time.monotonic() - start_time
        print(f"{func.__name__} {args} {kwargs}", "elapsed", elapsed)
        return result
    return wrapper


def run_postgres_stress_test(chunk_size: int) -> None:
    @elapsed
    def insert_data(cursor, chunk_size: int) -> None:
        for chunk in generate_test_data(chunk_size):
            cursor.execute(
                f"""
                INSERT INTO {settings.POSTGRES.TABLE_NAME} (id, ts, movie_id, user_id) 
                VALUES (%s, %s, %s, %s)
                """,
                *chunk
            )

    @elapsed
    def select_data(cursor) -> None:
        for _ in range(settings.SELECTS_QTY):
            random_id = random.randint(1, settings.ROWS_QTY)
            cursor.execute(f"SELECT * FROM {settings.POSTGRES.TABLE_NAME} WHERE id={random_id};")

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
    @elapsed
    def insert_data(client: Client, chunk_size: int) -> None:
        for chunk in generate_test_data(chunk_size):
            client.execute(
                f"INSERT INTO example.regular_table (id, ts, movie_id, user_id) VALUES",
                *chunk
            )

    @elapsed
    def select_data(client: Client) -> None:
        for _ in range(settings.SELECTS_QTY):
            random_id = random.randint(1, settings.ROWS_QTY)
            client.execute(
                f"SELECT * FROM example.regular_table WHERE (id == {random_id})"
            )

    client = Client(settings.CLICKHOUSE.HOST)
    client.execute("CREATE DATABASE IF NOT EXISTS example ON CLUSTER company_cluster")
    client.execute(
        "CREATE TABLE IF NOT EXISTS example.regular_table ON CLUSTER company_cluster "
        "(id Int64, ts Int32, movie_id Int64, user_id Int64)"
        " Engine=MergeTree() ORDER BY id"
    )

    insert_data(client=client, chunk_size=chunk_size)

    client.execute("TRUNCATE DATABASE example.regular_table ON CLUSTER company_cluster")

    insert_data(client=client, chunk_size=1)

    select_data(client=client)
