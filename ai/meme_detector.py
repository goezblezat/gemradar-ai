BLACKLIST = [
    "SOL",
    "USDC",
    "USDT",
    "ETH",
    "WETH",
    "BTC"
]


def check_token(symbol, name):

    symbol = symbol.upper()

    if symbol in BLACKLIST:
        return {
            "is_meme": False,
            "reason": "Blue chip token"
        }

    return {
        "is_meme": True,
        "reason": "Potential meme candidate"
    }
