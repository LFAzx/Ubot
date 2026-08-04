import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}crypto <coin>", "Cek harga crypto (USD & IDR)", "Utility")

ALIASES = {
    "btc": "bitcoin", "eth": "ethereum", "sol": "solana", "bnb": "binancecoin",
    "doge": "dogecoin", "xrp": "ripple", "ada": "cardano", "usdt": "tether",
    "usdc": "usd-coin", "ton": "the-open-network", "trx": "tron",
}


def _get_coin_id(coin):
    return ALIASES.get(coin.lower(), coin.lower())


def _fetch_price(coin):
    coin_id = _get_coin_id(coin)
    resp = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={"ids": coin_id, "vs_currencies": "usd,idr", "include_24hr_change": "true"},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    if coin_id not in data:
        raise Exception(f"Coin `{coin}` gak ditemukan.")
    return data[coin_id]


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}crypto (\S+)$"))
async def crypto_handler(event):
    coin = event.pattern_match.group(1)
    await event.edit("💰 Cek harga...")
    try:
        d = await asyncio.to_thread(_fetch_price, coin)
        usd = d.get("usd")
        idr = d.get("idr")
        change = d.get("usd_24h_change", 0) or 0
        arrow = "🟢" if change >= 0 else "🔴"
        await event.edit(
            f"💰 **{coin.upper()}**\n"
            f"${usd:,.2f} / Rp{idr:,.0f}\n"
            f"{arrow} 24h: {change:.2f}%"
        )
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
