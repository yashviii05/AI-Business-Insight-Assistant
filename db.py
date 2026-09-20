"""
db.py
-----
Handles the connection to your PostgreSQL database.
Every other file imports get_connection() from here instead of
connecting to Postgres directly — that way there's only one place
your credentials are used.
"""

import os
import psycopg2
from dotenv import load_dotenv

# Reads the .env file and makes its values available via os.getenv()
load_dotenv()


def get_connection():
    """
    Opens and returns a connection to the PostgreSQL database.
    Call this whenever you need to run a query.
    """
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


if __name__ == "__main__":
    # Quick manual test: run "python db.py" to check your credentials work.
    try:
        conn = get_connection()
        print("Connected successfully!")
        conn.close()
    except Exception as e:
        print("Connection failed:", e)
