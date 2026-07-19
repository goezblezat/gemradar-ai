from ai.gem_score import calculate_gem_score


result = calculate_gem_score(
    liquidity=77934,
    volume_24h=557,
    fdv=219280,
    risk="MEDIUM"
)


print(result)
