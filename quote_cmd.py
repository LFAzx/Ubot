import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}quote", "Quote random", "Fun")


def _fetch_quote():
    resp = requests.get("https://zenquotes.io/api/random", timeout=10)
    resp.raise_for_status()
    data = resp.json()[0]
    return f"{data['q']}\n— {data['a']}"


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}quote$"))
async def quote_handler(event):
    await event.edit("💬 Cari quote...")
    try:
        result = await asyncio.to_thread(_fetch_quote)
        await event.edit(f"💬 {result}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
