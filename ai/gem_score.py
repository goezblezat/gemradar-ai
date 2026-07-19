def calculate_gem_score(
    liquidity,
    volume_24h,
    fdv,
    risk
):

    score = 0


    # Liquidity Score
    if liquidity >= 100000:
        score += 30
    elif liquidity >= 50000:
        score += 25
    elif liquidity >= 10000:
        score += 15
    else:
        score += 5


    # Volume Score
    if volume_24h >= 1000000:
        score += 25
    elif volume_24h >= 100000:
        score += 20
    elif volume_24h >= 10000:
        score += 10
    else:
        score += 5


    # FDV Score
    if fdv <= 500000:
        score += 25
    elif fdv <= 5000000:
        score += 15
    else:
        score += 5


    # Risk Adjustment
    if risk == "LOW":
        score += 20
    elif risk == "MEDIUM":
        score += 10
    else:
        score -= 10


    # Maximum 100
    if score > 100:
        score = 100


    # Status
    if score >= 80:
        status = "🔥 HIDDEN GEM"
    elif score >= 60:
        status = "👀 WATCHLIST"
    elif score >= 40:
        status = "⚠️ RISKY"
    else:
        status = "❌ IGNORE"


    return {
        "gem_score": score,
        "status": status
    }
