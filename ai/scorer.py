def calculate_score(
    liquidity,
    volume,
    holders
):

    score = 0


    # Liquidity
    if liquidity >= 100000:
        score += 30
    elif liquidity >= 10000:
        score += 20
    else:
        score += 10


    # Volume
    if volume >= 500000:
        score += 30
    elif volume >= 50000:
        score += 20
    else:
        score += 10


    # Holders
    if holders >= 5000:
        score += 20
    elif holders >= 500:
        score += 15
    else:
        score += 10


    # Base safety score
    score += 20


    return score



if __name__ == "__main__":

    result = calculate_score(
        10000,
        50000,
        100
    )

    print("🤖 GemRadar AI Score")
    print("===================")
    print(f"Score : {result}/100")