import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}expand <short_url>", "Expand short URL, lihat tujuan aslinya", "Utility")


def _expand_url(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    resp = requests.head(url, allow_redirects=True, timeout=15)
    return resp.url


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}expand (\S+)$"))
async def expand_handler(event):
    url = event.pattern_match.group(1)
    await event.edit("🔗 Cek tujuan link...")
    try:
        final_url = await asyncio.to_thread(_expand_url, url)
        await event.edit(f"🔗 **Tujuan asli:**\n{final_url}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
