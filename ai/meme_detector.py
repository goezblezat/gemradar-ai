BLUE_CHIPS = [
    "SOLANA",
    "WRAPPED SOL",
    "USD COIN",
    "TETHER",
    "ETHEREUM",
    "BITCOIN"
]


def check_token(symbol, name):

    symbol = (symbol or "").upper()
    name = (name or "").upper()


    for coin in BLUE_CHIPS:
        if coin in name:
            return {
                "is_meme": False,
                "reason": "Blue chip token"
            }


    return {
        "is_meme": True,
        "reason": "Potential meme candidate"
    }
