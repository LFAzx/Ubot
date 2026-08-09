import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}dadjoke", "Random dad joke receh", "Fun")


def _get_dadjoke():
    resp = requests.get(
        "https://icanhazdadjoke.com/",
        headers={"Accept": "application/json"},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json().get("joke", "?")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}dadjoke$"))
async def dadjoke_handler(event):
    await event.edit("😂 Cari joke...")
    try:
        joke = await asyncio.to_thread(_get_dadjoke)
        await event.edit(f"😂 {joke}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
