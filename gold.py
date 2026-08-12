import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}gold", "Cek harga emas hari ini (per ons troy, USD)", "Utility")


def _get_gold_price():
    resp = requests.get("https://data-asg.goldprice.org/dbXRates/USD", timeout=15)
    resp.raise_for_status()
    data = resp.json()
    item = data["items"][0]
    return item.get("xauPrice"), item.get("chgXau"), item.get("pcXau")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}gold$"))
async def gold_handler(event):
    await event.edit("🥇 Cek harga emas...")
    try:
        price, change, change_pct = await asyncio.to_thread(_get_gold_price)
        arrow = "🟢" if change and change >= 0 else "🔴"
        await event.edit(
            f"🥇 **Harga Emas (per ons troy)**\n"
            f"${price:,.2f} USD\n"
            f"{arrow} {change:+.2f} ({change_pct:+.2f}%)"
        )
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
