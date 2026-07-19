
import requests

from ai.filter import analyze_token
from ai.meme_detector import check_token
from ai.gem_score import calculate_gem_score
from scanner.database_writer import save_token


URL = "https://api.dexscreener.com/latest/dex/search?q=SOL"


def get_tokens():

    response = requests.get(URL, timeout=10)

    if response.status_code != 200:
        print("❌ Failed to connect")
        return


    data = response.json()

    print("=" * 40)
    print("🚀 GemRadar DexScreener")
    print("=" * 40)


    pairs = data.get("pairs", [])


    if not pairs:
        print("No tokens found")
        return

    for pair in pairs[:10]:

        base = pair.get("baseToken", {})
        liquidity = pair.get("liquidity", {})
        volume = pair.get("volume", {})

        address = base.get("address")
        symbol = base.get("symbol")
        name = base.get("name")

        meme_check = check_token(
            symbol,
            name
        )

        if not meme_check["is_meme"]:
            print("❌ SKIP:", name, "-", meme_check["reason"])
            continue

        price = float(pair.get("priceUsd") or 0)

        liquidity_usd = float(liquidity.get("usd") or 0)

        volume24 = float(volume.get("h24") or 0)

        fdv = float(pair.get("fdv") or 0)


        analysis = analyze_token(
            symbol,
            liquidity_usd,
            volume24,
            fdv
        )


        ai_score = analysis["score"]
        risk_level = analysis["risk"]
        gem_analysis = calculate_gem_score(
            liquidity_usd,
            volume24,
            fdv,
            risk_level
        )

        gem_score = gem_analysis["gem_score"]
        gem_status = gem_analysis["status"]

        print("=" * 40)
        print("Token      :", symbol)
        print("Name       :", name)
        print("Liquidity  :", liquidity_usd)
        print("Volume 24h :", volume24)
        print("FDV        :", fdv)
        print("AI Score   :", ai_score)
        print("Risk       :", risk_level)
        print("Gem Score  :", gem_score)
        print("Status     :", gem_status)

        save_token(
            address,
            name,
            symbol,
            price,
            liquidity_usd,
            volume24,
            0,
            ai_score,
            fdv,
            "DexScreener",
            risk_level
        )


if __name__ == "__main__":
    get_tokens()
