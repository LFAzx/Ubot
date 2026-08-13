import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}currencylist", "List kode mata uang yang didukung .currency", "Utility")


def _get_currency_list():
    resp = requests.get("https://open.er-api.com/v6/latest/USD", timeout=15)
    resp.raise_for_status()
    data = resp.json()
    return sorted(data.get("rates", {}).keys())


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}currencylist$"))
async def currencylist_handler(event):
    await event.edit("💱 Ambil list currency...")
    try:
        codes = await asyncio.to_thread(_get_currency_list)
        text = ", ".join(codes)
        await event.edit(f"💱 **{len(codes)} kode currency didukung:**\n{text}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
