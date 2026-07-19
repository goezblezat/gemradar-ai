import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def connect_database():
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        print("✓ PostgreSQL Connected")
        return connection

    except Exception as error:
        print("✗ Database Connection Failed")
        print(error)


if __name__ == "__main__":
    connect_database()