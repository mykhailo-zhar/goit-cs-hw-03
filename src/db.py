import os
from contextlib import contextmanager

import psycopg2


@contextmanager
def create_connection():
    conn = psycopg2.connect(
        dbname="sample",
        user="postgres",
        password=os.environ.get("POSTGRES_PASSWORD"),
        host="localhost",  # or an IP address like '127.0.0.1'
        port=os.environ.get("POSTGRES_PORT", "5432"),  # default PostgreSQL port
    )

    yield conn
    conn.rollback()
    conn.close()
