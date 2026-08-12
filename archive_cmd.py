import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}archive <link>", "Simpan snapshot halaman web ke Wayback Machine", "Utility")


def _archive_url(url):
    resp = requests.get(f"https://web.archive.org/save/{url}", timeout=45, allow_redirects=True)
    resp.raise_for_status()
    return resp.url


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}archive (\S+)$"))
async def archive_handler(event):
    url = event.pattern_match.group(1)
    await event.edit("🗄️ Simpan ke Wayback Machine (bisa agak lama)...")
    try:
        archived_url = await asyncio.to_thread(_archive_url, url)
        await event.edit(f"🗄️ **Tersimpan:**\n{archived_url}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
