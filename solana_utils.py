import asyncio
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey

async def get_solana_balance(wallet_address):
    async with AsyncClient("https://api.mainnet-beta.solana.com") as client:
        try:
            public_key = Pubkey.from_string(wallet_address)
            response = await client.get_balance(public_key)
            return response.value / 10**9
        except Exception:
            return None

