from solana.rpc.async_api import AsyncClient
import asyncio


SOLANA_RPC = "https://api.mainnet-beta.solana.com"


async def connect_solana():

    client = AsyncClient(SOLANA_RPC)

    try:
        response = await client.get_slot()

        print("✓ Solana RPC Connected")
        print(f"✓ Current Slot: {response.value}")

    except Exception as error:
        print("✗ Solana Connection Failed")
        print(error)

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(connect_solana())