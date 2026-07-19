import asyncio
from solana.rpc.async_api import AsyncClient


SOLANA_RPC = "https://api.mainnet-beta.solana.com"


async def scan_latest_block():

    client = AsyncClient(SOLANA_RPC)

    try:
        slot = await client.get_slot()

        print("================================")
        print("🔎 GemRadar Token Scanner")
        print("================================")

        print(f"Current Slot : {slot.value}")
        print("✓ Scanner Online")

    except Exception as error:
        print(error)

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(scan_latest_block())