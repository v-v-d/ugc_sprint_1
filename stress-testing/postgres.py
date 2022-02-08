import psycopg2
import time
from psycopg2.extras import DictCursor


class PostgresStressTest:
    def __init__(self, pg_conn):
        self.pg_conn = pg_conn

    def save_all_data(self, data: list[object], table: str, rows_name: str):
        start_time = time.time()
        cursor = self.pg_conn.cursor()
        query = f"""INSERT INTO {table} ({rows_name})
                    VALUES %s ; """
        psycopg2.extras.execute_values(cur=cursor, sql=query, argslist=data, page_size=100)
        self.pg_conn.commit()
        print(time.time() - start_time)

    def search_data(self, table, id_obj):
        start_time = time.time()
        cursor = self.pg_conn.cursor()
        cursor.execute(
            f"""SELECT * FROM {table}
                WHERE id={id_obj}; """
        )
        print(time.time() - start_time)
