from db import create_connection


def execute_query(conn, sql, params=None):
    cur = conn.cursor()
    cur.execute(sql, params)
    return cur.fetchall()


def modification_query(conn, sql, params=None):
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()


# Отримати всі завдання певного користувача. Використайте SELECT для отримання завдань конкретного користувача за його user_id.
def select_all_tasks_of_user(conn, user_id):
    print(
        f"Selecting all tasks of user {user_id} \n",
        execute_query(
            conn,
            """
SELECT * FROM tasks WHERE user_id = %s
    """,
            (user_id,),
        ),
    )


# Вибрати завдання за певним статусом. Використайте підзапит для вибору завдань з конкретним статусом, наприклад, 'new'.
def select_all_tasks_with_status(conn, status):
    print(
        f"Selecting all tasks with status: {status} \n",
        execute_query(
            conn,
            "SELECT * FROM tasks WHERE status_id in (SELECT id from status WHERE name = %s)",
            (status,),
        ),
    )


# Оновити статус конкретного завдання. Змініть статус конкретного завдання на 'in progress' або інший статус.
def update_task_status(conn, task_id, status_id):
    cur = conn.cursor()
    cur.execute("SELECT name from status WHERE id = %s", (status_id,))
    status = cur.fetchone()[0]
    cur.execute(
        """
UPDATE tasks SET status_id = %s WHERE id = %s
RETURNING id, title;
    """,
        (status_id, task_id),
    )
    returned_row = cur.fetchone()
    conn.commit()
    print(f"Updated task #{returned_row[0]} {returned_row[1]} to status: {status} \n")


# Отримати список користувачів, які не мають жодного завдання. Використайте комбінацію SELECT, WHERE NOT IN і підзапит.
def users_without_tasks(conn):
    print(
        "Users without task: \n",
        execute_query(
            conn,
            """
SELECT * FROM users WHERE 
    id NOT IN
             (SELECT DISTINCT user_id from tasks);
    """,
        ),
    )


# Додати нове завдання для конкретного користувача. Використайте INSERT для додавання нового завдання.
def add_task(conn, title, description, user_id, status_id):
    cur = conn.cursor()
    cur.execute(
        """
INSERT INTO tasks(title, description, user_id, status_id) 
VALUES
(%s, %s, %s, %s)
RETURNING id;
    """,
        (title, description, user_id, status_id),
    )
    returned_row = cur.fetchone()
    print(f"Added task id: {returned_row[0]} \n")
    conn.commit()


# Отримати всі завдання, які ще не завершено. Виберіть завдання, чий статус не є 'завершено'.
def select_incomplete_tasks(conn):
    print(
        "Incomplete tasks: \n",
        execute_query(
            conn,
            """
SELECT * FROM tasks WHERE 
    status_id NOT IN
             (SELECT id from status WHERE name = 'completed');
    """,
        ),
    )
    print()


# Видалити конкретне завдання. Використайте DELETE для видалення завдання за його id.
def remove_task(conn, task_id):
    cur = conn.cursor()
    cur.execute(
        """
DELETE FROM tasks 
WHERE 
id = %s
RETURNING id;
    """,
        (task_id,),
    )
    returned_row = cur.fetchone()
    if returned_row:
        print(f"Removed task with id: {returned_row[0]} \n")
    else:
        print("Task does not exist\n")
    print()


# Знайти користувачів з певною електронною поштою. Використайте SELECT із умовою LIKE для фільтрації за електронною поштою.
def select_users_with_example_com(conn):
    print(
        "All users with example.com domain",
        execute_query(
            conn,
            """
SELECT * FROM users WHERE 
    email LIKE '%@example.com';
    """,
        ),
    )
    print()


# Оновити ім'я користувача. Змініть ім'я користувача за допомогою UPDATE.
def update_username(conn, user_id, newusername):
    cur = conn.cursor()
    cur.execute(
        """
UPDATE users 
SET fullname = %s
WHERE 
id = %s
RETURNING id, fullname;
    """,
        (newusername, user_id),
    )
    returned_row = cur.fetchone()
    conn.commit()
    print(f"Change user with id = {returned_row[0]} to {returned_row[1]} \n")


# Отримати кількість завдань для кожного статусу. Використайте SELECT, COUNT, GROUP BY для групування завдань за статусами.
def count_statuses(conn):
    print(
        "Statuses: \n",
        execute_query(
            conn,
            """
SELECT s.name, COUNT(*) FROM tasks as t JOIN status as s ON t.status_id = s.id
GROUP BY s.name
    """,
        ),
    )
    print()


# Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти. Використайте SELECT з умовою LIKE в поєднанні з JOIN, щоб вибрати завдання, призначені користувачам, чия електронна пошта містить певний домен (наприклад, '%@example.com').
def select_tasks_with_example_com(conn):
    print(
        "Tasks with users with domain - example.com: \n",
        execute_query(
            conn,
            """
SELECT t.id, t.title, t.description, u.email FROM tasks as t JOIN users as u ON t.user_id = u.id WHERE 
    u.email LIKE '%@example.com';
    """,
        ),
    )
    print()


# Отримати список завдань, що не мають опису. Виберіть завдання, у яких відсутній опис.
def select_tasks_with_no_desc(conn):
    print(
        "Tasks without description: \n",
        execute_query(
            conn,
            """
SELECT * FROM tasks WHERE 
    description IS NULL;
    """,
        ),
    )
    print()


# Вибрати користувачів та їхні завдання, які є у статусі 'in progress'. Використайте INNER JOIN для отримання списку користувачів та їхніх завдань із певним статусом.
def select_in_progress_tasks(conn):
    print(
        "In progress tasks: \n",
        execute_query(
            conn,
            """
SELECT t.id, t.title, t.description, u.email, s.name 
FROM tasks as t 
JOIN users as u ON t.user_id = u.id 
JOIN status as s ON t.status_id = s.id
WHERE 
    s.name = 'in progress';
    """,
        ),
    )
    print()


# Отримати користувачів та кількість їхніх завдань. Використайте LEFT JOIN та GROUP BY для вибору користувачів та підрахунку їхніх завдань.
def count_user_tasks(conn):
    print(
        "Tasks by users: \n",
        execute_query(
            conn,
            """
SELECT u.id || ' ' || u.fullname || '(' || u.email || ')', COUNT(t.id) 
FROM users as u 
LEFT JOIN tasks as t ON t.user_id = u.id
GROUP BY u.id;
    """,
        ),
    )
    print()


if __name__ == "__main__":
    with create_connection() as conn:
        if conn is not None:
            select_all_tasks_of_user(conn, 1)
            select_all_tasks_with_status(conn, "new")
            update_task_status(conn, 6, 2)
            users_without_tasks(conn)
            print('\n Adding new task: "New task" with status Done to Charlie')
            add_task(conn, "New task", "New task description", 6, 3)
            select_incomplete_tasks(conn)
            remove_task(conn, 5)
            select_users_with_example_com(conn)
            update_username(conn, 4, "Lessley")
            count_statuses(conn)
            print()
            select_tasks_with_example_com(conn)
            select_tasks_with_no_desc(conn)
            select_in_progress_tasks(conn)
            count_user_tasks(conn)
        else:
            print("Error! cannot create the database connection.")
