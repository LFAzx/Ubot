import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}stock <ticker>", "Cek harga saham (misal AAPL, BBCA.JK)", "Utility")


def _get_stock(ticker):
    resp = requests.get(
        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}",
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    result = data["chart"]["result"][0]
    meta = result["meta"]
    price = meta.get("regularMarketPrice")
    prev_close = meta.get("previousClose") or meta.get("chartPreviousClose")
    currency = meta.get("currency", "")
    change = (price - prev_close) if price and prev_close else 0
    change_pct = (change / prev_close * 100) if prev_close else 0
    return price, change, change_pct, currency


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}stock (\S+)$"))
async def stock_handler(event):
    ticker = event.pattern_match.group(1).upper()
    await event.edit("📈 Cek harga saham...")
    try:
        price, change, change_pct, currency = await asyncio.to_thread(_get_stock, ticker)
        arrow = "🟢" if change >= 0 else "🔴"
        await event.edit(
            f"📈 **{ticker}**\n"
            f"{price:,.2f} {currency}\n"
            f"{arrow} {change:+,.2f} ({change_pct:+.2f}%)"
        )
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
