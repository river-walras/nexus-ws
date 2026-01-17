import asyncio
import msgspec
import requests
from typing import Literal
from nexus_ws import BybitWSClient, BybitStreamUrl


def get_instrument_info(
    category: Literal["spot", "linear", "inverse", "option"],
    status: Literal["PreLaunch", "Trading", "Delivering", "Closed"] | None = None,
) -> list[str]:
    """
    /v5/market/instruments-info
    """
    url = "https://api.bybit.com/v5/market/instruments-info"
    params = {"category": category, "limit": 1000}
    if status is not None:
        params["status"] = status
    symbols: list[str] = []
    cursor: str | None = None
    while True:
        if cursor:
            params["cursor"] = cursor
        else:
            params.pop("cursor", None)
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("retCode") != 0:
            raise RuntimeError(f"Bybit API error: {data}")
        result = data.get("result", {})
        symbols.extend(item["symbol"] for item in result.get("list", []))
        cursor = result.get("nextPageCursor") or None
        if not cursor:
            break
    return symbols


def handler(raw: bytes):
    message = msgspec.json.decode(raw)
    print("Received message:", message)


async def main():
    url = BybitStreamUrl.OPTION
    client = BybitWSClient(handler, url, max_subscriptions_per_client=50, max_clients=20)

    symbols = get_instrument_info("option", "Trading")

    client.subscribe_trade(symbols)
    client.subscribe_order_book(symbols, "25")
    await client.wait(timeout=1000)


if __name__ == "__main__":
    asyncio.run(main())
