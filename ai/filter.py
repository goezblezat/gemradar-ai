def analyze_token(
    symbol,
    liquidity,
    volume_24h,
    fdv
):

    score = 0
    risk = "HIGH"


    # Liquidity check
    if liquidity >= 10000:
        score += 30

    if liquidity >= 50000:
        score += 10


    # Volume check
    if volume_24h >= 10000:
        score += 20

    if volume_24h >= 100000:
        score += 10


    # FDV check
    if fdv <= 5000000:
        score += 20


    # Risk level
    if score >= 70:
        risk = "LOW"

    elif score >= 40:
        risk = "MEDIUM"


    return {
        "score": score,
        "risk": risk
    }