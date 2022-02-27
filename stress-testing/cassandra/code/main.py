import time
from typing import Callable, Any, Generator, Optional, Union

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster, Session
from cassandra.query import PreparedStatement
from mimesis import Generic

DB_USERNAME: str = "cassandra"
DB_PASSWD: str = "cassandra"
NODES: tuple[str, ...] = "cassandra1", "cassandra2", "cassandra3"
KEYSPACE: str = "test_keyspace"
RATING_MIN_VAL: int = 1
RATING_MAX_VAL: int = 10
SENTENCES_QTY: int = 20
CHUNK_SIZE: int = 1000
ROWS_QTY: int = 1000000
OPERATIONS_QTY: int = 5
TEST_DATA_TYPE = list[Union[str, int]]

fake = Generic()

FILM_IDS_USER_IDS_CONTAINER: list[list[str, ...]] = [
    [fake.cryptographic.uuid_object(), fake.cryptographic.uuid_object()]
    for _ in range(ROWS_QTY)
]

session: Optional[Session] = None
auth = PlainTextAuthProvider(username=DB_USERNAME, password=DB_PASSWD)
cluster = Cluster(NODES, auth_provider=auth)


def elapsed(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        elapsed = time.monotonic() - start_time

        with open("result/stress-testing.txt", "a", encoding="utf-8") as f:
            f.write(f"{func.__name__} {args} {kwargs} elapsed {elapsed} \n")

        return result

    return wrapper


def create_tables() -> None:
    session.execute(
        """
        CREATE KEYSPACE IF NOT EXISTS test_keyspace
        WITH REPLICATION = { 
            'class' : 'SimpleStrategy', 
            'replication_factor' : 3 
        };
    """
    )

    session.set_keyspace(KEYSPACE)

    session.execute(
        """
    CREATE TABLE IF NOT EXISTS film_ratings (
        id uuid,
        film_id uuid,
        user_id uuid,
        rating int,
        created_at timestamp,
        updated_at timestamp,
        PRIMARY KEY (id)
    );
    """
    )

    session.execute(
        """
    CREATE TABLE IF NOT EXISTS film_reviews (
        id uuid,
        film_id uuid,
        user_id uuid,
        text text,
        rating int,
        created_at timestamp,
        updated_at timestamp,
        PRIMARY KEY (id)
    );
    """
    )

    session.execute(
        """
    CREATE TABLE IF NOT EXISTS bookmarks (
        id uuid,
        film_id uuid,
        user_id uuid,
        created_at timestamp,
        PRIMARY KEY (id)
    );
    """
    )


def get_film_rating_data() -> TEST_DATA_TYPE:
    rating = fake.numeric.integer_number(start=RATING_MIN_VAL, end=RATING_MAX_VAL)
    created_at = fake.datetime.timestamp(start=fake.datetime.CURRENT_YEAR)
    updated_at = fake.datetime.timestamp(start=fake.datetime.CURRENT_YEAR)

    return [rating, created_at, updated_at]


def get_film_review_data() -> TEST_DATA_TYPE:
    text = fake.text.text(quantity=SENTENCES_QTY)
    rating = fake.numeric.integer_number(start=RATING_MIN_VAL, end=RATING_MAX_VAL)
    created_at = fake.datetime.timestamp(start=fake.datetime.CURRENT_YEAR)
    updated_at = fake.datetime.timestamp(start=fake.datetime.CURRENT_YEAR)

    return [text, rating, created_at, updated_at]


def get_bookmark_data() -> TEST_DATA_TYPE:
    return [fake.datetime.timestamp(start=fake.datetime.CURRENT_YEAR)]


def generate_test_data(
    data_builder: Callable,
) -> Generator[list[TEST_DATA_TYPE], None, None]:
    chunk = []

    for data in FILM_IDS_USER_IDS_CONTAINER:
        data = [fake.cryptographic.uuid_object(), *data]
        extra_data = data_builder()
        data.extend(extra_data)
        chunk.append(data)

        if len(chunk) == CHUNK_SIZE:
            yield chunk
            chunk = []

    yield chunk


def insert_test_data(data_builder: Callable, insert_stmt: PreparedStatement) -> None:
    for chunk in generate_test_data(data_builder):
        for row in chunk:
            session.execute(insert_stmt, row)
        print(
            f"Data chunk loaded with size {len(chunk)} and stmt {insert_stmt.query_string}."
        )


@elapsed
def insert_film_ratings():
    stmt = session.prepare(
        "INSERT INTO film_ratings (id,film_id,user_id,rating,created_at,updated_at) VALUES (?,?,?,?,?,?)"
    )
    insert_test_data(get_film_rating_data, stmt)


@elapsed
def insert_film_reviews():
    stmt = session.prepare(
        "INSERT INTO film_reviews (id,film_id,user_id,text,rating,created_at,updated_at) VALUES (?,?,?,?,?,?,?)"
    )
    insert_test_data(get_film_review_data, stmt)


@elapsed
def insert_bookmarks():
    stmt = session.prepare(
        "INSERT INTO bookmarks (id,film_id,user_id,created_at) VALUES (?,?,?,?)"
    )
    insert_test_data(get_bookmark_data, stmt)


@elapsed
def select_rated_films_by_user(user_id: str):
    like_threshold = int(RATING_MAX_VAL / 2)
    query = f"SELECT * FROM film_ratings WHERE user_id={user_id} AND rating >= {like_threshold} ALLOW FILTERING"
    session.execute(query)
    print("select_rated_films_by_user done.")


@elapsed
def select_film_ratings_qty(film_id: str):
    like_threshold = int(RATING_MAX_VAL / 2)
    query = f"SELECT count(*) FROM film_ratings WHERE film_id={film_id} AND rating >= {like_threshold} ALLOW FILTERING"
    session.execute(query)
    print("select_film_ratings_qty done.")


@elapsed
def select_bookmarks_by_user(user_id: str):
    query = f"SELECT * FROM bookmarks WHERE user_id={user_id} ALLOW FILTERING"
    session.execute(query)
    print("select_bookmarks_by_user done.")


@elapsed
def select_film_avg_rating(film_id: str):
    query = f"SELECT film_id, Avg(rating) FROM film_ratings WHERE film_id={film_id} ALLOW FILTERING"
    session.execute(query)
    print("select_film_avg_rating done.")


@elapsed
def insert_and_select_film_new_rating(film_id: str, user_id: str):
    stmt = session.prepare(
        "INSERT INTO film_ratings (id,film_id,user_id,rating,created_at,updated_at) VALUES (?,?,?,?,?,?)"
    )

    data = [fake.cryptographic.uuid_object(), film_id, user_id]
    extra_data = get_film_rating_data()
    data.extend(extra_data)

    session.execute(stmt, data)
    print("insert_and_select_film_new_rating done.")


def main():
    global session

    session = cluster.connect()

    try:
        create_tables()
        insert_film_ratings()
        insert_film_reviews()
        insert_bookmarks()

        for film_id, user_id in FILM_IDS_USER_IDS_CONTAINER[:OPERATIONS_QTY]:
            select_rated_films_by_user(user_id)
            select_film_ratings_qty(film_id)
            select_bookmarks_by_user(user_id)
            select_film_avg_rating(film_id)
            insert_and_select_film_new_rating(film_id, user_id)

    finally:
        if session is not None:
            session.shutdown()


if __name__ == "__main__":
    main()
