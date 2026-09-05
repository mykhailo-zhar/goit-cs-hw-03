# Task manager (PostgreSQL) and cats CRUD (MongoDB)

Homework scripts: PostgreSQL tables, seed data, and SQL queries for a task manager; PyMongo CRUD for cat documents.

## Setup

1. Install [mise](https://mise.jdx.dev/getting-started.html) and activate it in your shell.
2. From the repo root:

```bash
mise trust
mise install
uv sync
```

3. Create `mise.local.toml` (see [Environment](#environment)). mise loads it automatically.
4. Start PostgreSQL (`dbname=sample`, user `postgres`, host `localhost`):

```bash
docker compose up -d
```

5. Seed PostgreSQL, then run both demos:

```bash
python src/seed.py
python main.py
```

`main.py` runs the PostgreSQL query demo, then the MongoDB CRUD demo (the latter asks for a cat name).

## Environment

Connection settings are read in [`src/db.py`](src/db.py). Put secrets in **`mise.local.toml`** (gitignored). Do not commit real passwords.

| Variable | Used by | Description |
|---|---|---|
| `POSTGRES_PASSWORD` | PostgreSQL | Password for user `postgres`. Also used by `docker-compose.yml`. |
| `POSTGRES_PORT` | PostgreSQL | Host port. Defaults to `5432` if unset. |
| `MONGODB_USER` | MongoDB Atlas | Database user. |
| `MONGODB_PASSWORD` | MongoDB Atlas | Database password. |
| `MONGODB_HOST` | MongoDB Atlas | Cluster host, for example `cluster0.xxxxx.mongodb.net`. |
| `MONGODB_APPNAME` | MongoDB Atlas | `appName` query parameter (cluster name). |

PostgreSQL database name (`sample`), user (`postgres`), and host (`localhost`) are hardcoded. MongoDB uses database `cats`.

Sample `mise.local.toml`:

```toml
[env]
POSTGRES_PASSWORD = "password"
POSTGRES_PORT = "5432"
MONGODB_USER = "your_mongodb_user"
MONGODB_PASSWORD = "your_mongodb_password"
MONGODB_HOST = "cluster0.xxxxx.mongodb.net"
MONGODB_APPNAME = "Cluster0"
```

Copy this file to the project root, replace the placeholders, then re-enter the directory or run `mise set` so the env is loaded.

## Scripts

### PostgreSQL — [`src/seed.py`](src/seed.py)

- `create_tables` — drop and recreate `users`, `status`, `tasks` (unique email/name, `ON DELETE CASCADE` for a user's tasks).
- `seed_db` — fill tables with Faker data and statuses `new`, `in progress`, `completed`.
- `duplicates` — show that unique constraints reject duplicate email/status.

### PostgreSQL — [`src/queries.py`](src/queries.py)

- `select_all_tasks_of_user` — tasks for a `user_id`.
- `select_all_tasks_with_status` — tasks by status name (subquery).
- `update_task_status` — set a task's status.
- `users_without_tasks` — users with no tasks (`NOT IN`).
- `add_task` — insert a task for a user.
- `select_incomplete_tasks` — tasks not in status `completed`.
- `remove_task` — delete a task by id.
- `select_users_with_example_com` — users whose email matches `%@example.com`.
- `update_username` — change a user's full name.
- `count_statuses` — task counts grouped by status.
- `select_tasks_with_example_com` — tasks for users on `%@example.com` (`JOIN` + `LIKE`).
- `select_tasks_with_no_desc` — tasks with `description IS NULL`.
- `select_in_progress_tasks` — users and tasks in status `in progress`.
- `count_user_tasks` — users and their task counts (`LEFT JOIN`).

Helpers: `execute_query`, `modification_query`. Connection: `create_connection` in [`src/db.py`](src/db.py).

### MongoDB — [`src/mongo.py`](src/mongo.py)

Cat documents: `name`, `age`, `features`.

- `create_cats` — insert sample cats (Faker).
- `get_all_cats` — print the collection.
- `find_all_with_name` — find a cat by name.
- `update_cat_age` — set age by name.
- `add_cat_feature` — `$push` a feature by name.
- `remove_cat_with_name` — delete one cat by name.
- `remove_all_cats` — delete the collection.

PyMongo errors are caught by `error_decorator`. Connection: `create_mongo_connection` in [`src/db.py`](src/db.py).

## License

See [LICENSE](LICENSE).
