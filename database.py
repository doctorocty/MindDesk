import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    )


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id SERIAL PRIMARY KEY,

            full_name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (

            id SERIAL PRIMARY KEY,

            user_id INTEGER NOT NULL
                REFERENCES users(id)
                ON DELETE CASCADE,

            title TEXT NOT NULL,

            description TEXT,

            target_date DATE,

            progress INTEGER DEFAULT 0,

            completed BOOLEAN DEFAULT FALSE,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (

            id SERIAL PRIMARY KEY,

            user_id INTEGER NOT NULL
                REFERENCES users(id)
                ON DELETE CASCADE,

            title TEXT NOT NULL,

            description TEXT,

            due_date DATE,

            priority TEXT DEFAULT 'medium',

            completed BOOLEAN DEFAULT FALSE,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)
    connection.commit()

    cursor.close()

    connection.close()


def email_exists(email):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(

        "SELECT id FROM users WHERE email = %s",

        (email,)

    )

    user = cursor.fetchone()

    cursor.close()

    connection.close()

    return user is not None


def create_user(full_name, email, hashed_password):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(

        """
        INSERT INTO users
        (full_name, email, password)
        VALUES (%s, %s, %s)
        """,

        (full_name, email, hashed_password)

    )

    connection.commit()

    cursor.close()

    connection.close()


def get_user_by_email(email):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(

        """
        SELECT *
        FROM users
        WHERE email = %s
        """,

        (email,)

    )

    user = cursor.fetchone()

    cursor.close()

    connection.close()

    return user

def create_task(user_id, title, description=None, due_date=None, priority="medium"):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tasks
        (user_id, title, description, due_date, priority)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *
        """,
        (
            user_id,
            title,
            description,
            due_date,
            priority
        )
    )

    task = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    return task


def get_tasks(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM tasks
        WHERE user_id = %s
        ORDER BY completed ASC, due_date ASC NULLS LAST, created_at DESC
        """,
        (user_id,)
    )

    tasks = cursor.fetchall()

    cursor.close()
    connection.close()

    return tasks


def get_today_tasks(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM tasks
        WHERE user_id = %s
        AND due_date = CURRENT_DATE
        ORDER BY completed ASC, created_at DESC
        """,
        (user_id,)
    )

    tasks = cursor.fetchall()

    cursor.close()
    connection.close()

    return tasks


def toggle_task(task_id, user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET completed = NOT completed
        WHERE id = %s
        AND user_id = %s
        RETURNING *
        """,
        (task_id, user_id)
    )

    task = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    return task


def delete_task(task_id, user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM tasks
        WHERE id = %s
        AND user_id = %s
        RETURNING id
        """,
        (task_id, user_id)
    )

    deleted = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    return deleted


def get_task_counts(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_tasks,
            COUNT(*) FILTER (
                WHERE completed = TRUE
            ) AS completed_tasks
        FROM tasks
        WHERE user_id = %s
        """,
        (user_id,)
    )

    counts = cursor.fetchone()

    cursor.close()
    connection.close()

    return counts

def create_goal(
    user_id,
    title,
    description=None,
    target_date=None
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO goals
        (
            user_id,
            title,
            description,
            target_date
        )
        VALUES (%s, %s, %s, %s)
        RETURNING *
        """,
        (
            user_id,
            title,
            description,
            target_date
        )
    )

    goal = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    return goal


def get_goals(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM goals
        WHERE user_id = %s
        ORDER BY completed ASC,
                 target_date ASC NULLS LAST,
                 created_at DESC
        """,
        (user_id,)
    )

    goals = cursor.fetchall()

    cursor.close()
    connection.close()

    return goals


def get_active_goals(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM goals
        WHERE user_id = %s
        AND completed = FALSE
        ORDER BY target_date ASC NULLS LAST,
                 created_at DESC
        """,
        (user_id,)
    )

    goals = cursor.fetchall()

    cursor.close()
    connection.close()

    return goals


def update_goal_progress(
    goal_id,
    user_id,
    progress
):

    progress = max(
        0,
        min(100, int(progress))
    )

    completed = progress >= 100

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE goals
        SET
            progress = %s,
            completed = %s
        WHERE id = %s
        AND user_id = %s
        RETURNING *
        """,
        (
            progress,
            completed,
            goal_id,
            user_id
        )
    )

    goal = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    return goal


def delete_goal(
    goal_id,
    user_id
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM goals
        WHERE id = %s
        AND user_id = %s
        RETURNING id
        """,
        (
            goal_id,
            user_id
        )
    )

    deleted = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    return deleted


def get_goal_counts(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_goals,
            COUNT(*) FILTER (
                WHERE completed = FALSE
            ) AS active_goals,
            COUNT(*) FILTER (
                WHERE completed = TRUE
            ) AS completed_goals
        FROM goals
        WHERE user_id = %s
        """,
        (user_id,)
    )

    counts = cursor.fetchone()

    cursor.close()
    connection.close()

    return counts