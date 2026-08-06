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