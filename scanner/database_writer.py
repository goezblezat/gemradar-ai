from app.database import connect_database


def save_token(
    address,
    name,
    symbol,
    price=0,
    liquidity=0,
    volume_24h=0,
    holders=0,
    ai_score=0,
    fdv=0,
    source="DexScreener",
    risk_level="UNKNOWN"
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
            ai_score,
            fdv,
            source,
            risk_level
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

        ON CONFLICT (address)
        DO UPDATE SET
            price = EXCLUDED.price,
            liquidity = EXCLUDED.liquidity,
            volume_24h = EXCLUDED.volume_24h,
            ai_score = EXCLUDED.ai_score,
            fdv = EXCLUDED.fdv,
            source = EXCLUDED.source,
            risk_level = EXCLUDED.risk_level;
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
                ai_score,
                fdv,
                source,
                risk_level
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
        70,
        50000,
        "Test",
        "LOW"
    )