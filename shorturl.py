import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}short <url>", "Bikin URL jadi pendek (TinyURL)", "Utility")


def _shorten(url):
    resp = requests.get("https://tinyurl.com/api-create.php", params={"url": url}, timeout=10)
    resp.raise_for_status()
    return resp.text.strip()


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}short (\S+)$"))
async def short_handler(event):
    url = event.pattern_match.group(1)
    await event.edit("🔗 Memendekkan URL...")
    try:
        result = await asyncio.to_thread(_shorten, url)
        await event.edit(f"🔗 {result}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
