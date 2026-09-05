from faker import Faker
from psycopg2 import Error

from db import create_connection


def create_tables(conn):
    """create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """

    queries = [
        "DROP TABLE IF EXISTS tasks, users, status CASCADE;",
        """
CREATE TABLE users(
  id SERIAL PRIMARY KEY,
  fullname VARCHAR(100),
  email VARCHAR(100) NOT NULL UNIQUE
);
""",
        """
CREATE TABLE status(
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE
);
""",
        """
CREATE TABLE tasks(
  id SERIAL PRIMARY KEY,
  title VARCHAR(100),
  description TEXT,
  status_id INT REFERENCES status (id) 
  ON UPDATE CASCADE
  ON DELETE CASCADE,
  user_id INT REFERENCES users (id) 
  ON UPDATE CASCADE
  ON DELETE CASCADE
);
""",
    ]
    try:
        c = conn.cursor()
        for query in queries:
            c.execute(query)
        conn.commit()
    except Error as e:
        print(e)


def seed_db(conn):
    fake = Faker()
    queries = [
        (
            """
INSERT INTO users(fullname, email)
VALUES
(%s, %s);""",
            [(fake.name(), fake.email()) for _ in range(5)]
            + [("Charlie", "charlie@example.com")],
        ),
        (
            """
INSERT INTO status(name)
VALUES
(%s);""",
            [("todo",), ("in progress",), ("done",)],
        ),
        (
            """
INSERT INTO tasks(title, description, status_id, user_id)
VALUES
(%s, %s, %s, %s)
""",
            [
                (fake.name(), "Description for task 1", 1, 1),
                (fake.name(), None, 1, 2),
                (fake.name(), "Description for task 3", 3, 3),
                (fake.name(), "Description for task 4", 2, 2),
                (fake.name(), "Description for task 5", 1, 1),
            ],
        ),
    ]
    try:
        c = conn.cursor()
        for query, params in queries:
            c.executemany(query, params)
        conn.commit()
    except Error as e:
        print(e)


def duplicates(conn):
    queries = [
        """
INSERT INTO status(name)
VALUES
('todo');  
""",
        """
INSERT INTO users(fullname, email)
VALUES
('Alice Smith', 'charlie@example.com');
    """,
    ]
    c = conn.cursor()
    for query in queries:
        try:
            c.execute(query)
        except Error as e:
            print(e)
        finally:
            conn.commit()


def main():
    with create_connection() as conn:
        if conn is not None:
            create_tables(conn)
            seed_db(conn)
            print("Will show duplicates")
            duplicates(conn)
        else:
            print("Error! cannot create the database connection.")


if __name__ == "__main__":
    main()
