import requests
import msgspec
import asyncio
from nexus_ws import BinanceWSClient, BinanceStreamUrl


def get_all_symbols():
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    response = requests.get(url)
    data = response.json()
    symbols = [
        item["symbol"] for item in data["symbols"] if item["status"] == "TRADING"
    ]
    return symbols


def handler(raw: bytes):
    message = msgspec.json.decode(raw)
    print("Received message:", message)


async def main():
    symbols = get_all_symbols()
    url = BinanceStreamUrl.USD_M_FUTURES
    async with BinanceWSClient(
        handler, url, max_clients=30, max_subscriptions_per_client=50
    ) as client:
        client.subscribe_trade(symbols)
        await asyncio.sleep(200)


if __name__ == "__main__":
    asyncio.run(main())
