import asyncio
import os
import msgspec
from dotenv import load_dotenv
from nexus_ws import BinanceWSApiClient, BinanceWsApiUrl


load_dotenv()

API_KEY = os.getenv("BNC_API_KEY")  
SECRET = os.getenv("BNC_SECRET")

def handler(raw: bytes):
    message = msgspec.json.decode(raw)
    print("Received message:", message)


async def main():
    url = BinanceWsApiUrl.SPOT_TESTNET
    async with BinanceWSApiClient(handler, url, API_KEY, SECRET) as client:
        client.subscribe_spot_user_data_stream()
        await asyncio.sleep(10000)


if __name__ == "__main__":
    asyncio.run(main())
