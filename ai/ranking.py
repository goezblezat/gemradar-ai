from app.database import connect_database


def get_top_gems(limit=10):

    connection = connect_database()

    if not connection:
        return []

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            name,
            symbol,
            liquidity,
            volume_24h,
            fdv,
            ai_score,
            risk_level,
            gem_score,
            gem_status
        FROM tokens
        WHERE gem_score IS NOT NULL
        ORDER BY gem_score DESC, ai_score DESC
        LIMIT %s;
    """, (limit,))

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return rows


if __name__ == "__main__":

    gems = get_top_gems()

    print("=" * 40)
    print("💎 GEMRADAR TOP GEMS")
    print("=" * 40)

    for i, gem in enumerate(gems, start=1):

        print(f"\n#{i}")
        print("Token      :", gem[0])
        print("Symbol     :", gem[1])
        print("Liquidity  :", gem[2])
        print("Volume24h  :", gem[3])
        print("FDV        :", gem[4])
        print("AI Score   :", gem[5])
        print("Risk       :", gem[6])
        print("Gem Score  :", gem[7])
        print("Status     :", gem[8])