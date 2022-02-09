import psycopg2
import time
import random
from psycopg2.extras import DictCursor
from locust import task


class PostgresStressTest:
    def __init__(self, pg_conn):
        self.pg_conn = pg_conn

    def save_all_data(self, data: list[object], table: str, rows_name: str):
        start_time = time.time()
        cursor = self.pg_conn.cursor()
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {table} (
                      id INT,
                      timestamp INT,
                      move_id INT,
                      user_id INT
                    );"""
        )
        query = f"""INSERT INTO {table} ({rows_name})
                    VALUES %s ; """
        psycopg2.extras.execute_values(
            cur=cursor, sql=query, argslist=data, page_size=100
        )
        self.pg_conn.commit()
        print(time.time() - start_time)

    def search_data(self, table):
        start_time = time.time()
        cursor = self.pg_conn.cursor()
        for i in range(101):
            cursor.execute(
                f"""SELECT * FROM {table}
                    WHERE id={random.randint(1, 9999999)}; """
            )
        print(time.time() - start_time)
