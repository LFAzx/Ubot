import os
import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}gifsearch <teks>", "Cari GIF dari Tenor", "Media")

TENOR_API_KEY = os.environ.get("TENOR_API_KEY")


def _search_gif(query):
    resp = requests.get(
        "https://tenor.googleapis.com/v2/search",
        params={"q": query, "key": TENOR_API_KEY, "limit": 1, "media_filter": "gif"},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    results = data.get("results", [])
    if not results:
        return None
    return results[0]["media_formats"]["gif"]["url"]


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}gifsearch (.+)$"))
async def gifsearch_handler(event):
    if not TENOR_API_KEY:
        await event.edit("⚠️ TENOR_API_KEY belum di-set di environment variable Railway.")
        return

    query = event.pattern_match.group(1)
    await event.edit("🔍 Cari GIF...")
    try:
        gif_url = await asyncio.to_thread(_search_gif, query)
        if not gif_url:
            await event.edit("❌ Gak nemu GIF.")
            return
        await event.delete()
        await client.send_file(event.chat_id, gif_url, caption=f"🔍 {query}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
