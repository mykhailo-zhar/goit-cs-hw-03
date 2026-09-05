import os
from contextlib import contextmanager

import psycopg2
from pymongo import MongoClient
from pymongo.server_api import ServerApi


@contextmanager
def create_connection():
    """Yield a PostgreSQL connection and roll it back when the block ends.

    Connection parameters come from POSTGRES_PASSWORD and POSTGRES_PORT.
    """
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


def create_mongo_connection():
    """Create a MongoDB client and return the cats database.

    Credentials are read from MONGODB_USER, MONGODB_PASSWORD, MONGODB_HOST,
    and MONGODB_APPNAME.
    """
    client = MongoClient(
        "mongodb+srv://{username}:{password}@{host}?appName={db}&retryWrites=true&w=majority".format(
            username=os.environ.get("MONGODB_USER"),
            password=os.environ.get("MONGODB_PASSWORD"),
            host=os.environ.get("MONGODB_HOST"),
            db=os.environ.get("MONGODB_APPNAME"),
        ),
        server_api=ServerApi("1"),
    )
    db = client.cats
    return db
