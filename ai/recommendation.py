def get_recommendation(
    gem_score,
    ai_score,
    risk,
    liquidity,
    volume,
    fdv
):

    reasons = []

    if liquidity >= 50000:
        reasons.append("✅ High Liquidity")

    if volume >= 10000:
        reasons.append("✅ Strong Volume")

    if fdv <= 500000:
        reasons.append("✅ Low FDV")

    if risk == "LOW":
        reasons.append("✅ Low Risk")

    if gem_score >= 80:
        signal = "🔥 STRONG BUY"
    elif gem_score >= 60:
        signal = "👀 WATCH"
    else:
        signal = "❌ SKIP"

    return {
        "signal": signal,
        "reasons": reasons
    }