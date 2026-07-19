from app.database import connect_database
from ai.scorer import calculate_score


def analyze_tokens():

    connection = connect_database()

    if connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, liquidity, volume_24h, holders
            FROM tokens;
        """)

        tokens = cursor.fetchall()


        for token in tokens:

            token_id = token[0]
            liquidity = float(token[1])
            volume = float(token[2])
            holders = token[3]


            score = calculate_score(
                liquidity,
                volume,
                holders
            )


            cursor.execute("""
                UPDATE tokens
                SET ai_score=%s
                WHERE id=%s;
            """,
            (
                score,
                token_id
            ))


            print(
                f"✓ Token {token_id} AI Score: {score}"
            )


        connection.commit()

        cursor.close()
        connection.close()


if __name__ == "__main__":
    analyze_tokens()