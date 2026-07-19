from database import connect_database


def create_tables():
    connection = connect_database()

    if connection:
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            id SERIAL PRIMARY KEY,
            address TEXT UNIQUE NOT NULL,
            name TEXT,
            symbol TEXT,
            price NUMERIC,
            liquidity NUMERIC,
            volume_24h NUMERIC,
            holders INTEGER,
            ai_score INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        connection.commit()

        cursor.close()
        connection.close()

        print("✓ Table tokens created")


if __name__ == "__main__":
    create_tables()