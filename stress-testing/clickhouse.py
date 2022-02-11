import time
import random
from clickhouse_driver import Client


class ClickHouse:
    def __init__(self, client: Client):
        self.client = client

    def save_all_data(self, data):
        start_time = time.time()
        self.client.execute(
            'CREATE DATABASE IF NOT EXISTS example ON CLUSTER company_cluster'

        )
        self.client.execute(
            'CREATE TABLE IF NOT EXISTS example.regular_table ON CLUSTER company_cluster '
            '(id Int64, time_stop Int32, move_id Int64, user_id Int64)'
            ' Engine=MergeTree() ORDER BY id'
        )
        data = ', '.join(map(str, data))
        self.client.execute(
            f'INSERT INTO example.regular_table (id, timestamp, move_id, user_id) VALUES {data}'
        )
        print(time.time() - start_time)

    def search_clickhouse(self):
        start_time = time.time()
        for i in range(101):
            self.client.execute(
                f'SELECT * FROM example.regular_table WHERE (id == {random.randint(1, 999999)})'
            )
        print(time.time() - start_time)
