from app.database import connect_database


def save_token(
    address,
    name,
    symbol,
    price=0,
    liquidity=0,
    volume_24h=0,
    holders=0,
    ai_score=0
):

    connection = connect_database()

    if connection:

        cursor = connection.cursor()

        query = """
        INSERT INTO tokens
        (
            address,
            name,
            symbol,
            price,
            liquidity,
            volume_24h,
            holders,
            ai_score
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (address)
        DO NOTHING;
        """

        cursor.execute(
            query,
            (
                address,
                name,
                symbol,
                price,
                liquidity,
                volume_24h,
                holders,
                ai_score
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        print("✓ Token Saved")


if __name__ == "__main__":

    save_token(
        "TEST123",
        "GemRadar Test",
        "GEM",
        0.01,
        10000,
        50000,
        100,
        75
    )