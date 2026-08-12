import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}waybackurls <domain>", "List URL historis yang pernah ke-index Wayback Machine", "OSINT")


def _get_wayback_urls(domain):
    resp = requests.get(
        "https://web.archive.org/cdx/search/cdx",
        params={"url": f"{domain}/*", "output": "json", "fl": "original", "collapse": "urlkey", "limit": 30},
        timeout=20,
    )
    resp.raise_for_status()
    data = resp.json()
    if not data or len(data) <= 1:
        return []
    return [row[0] for row in data[1:]]


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}waybackurls (\S+)$"))
async def waybackurls_handler(event):
    domain = event.pattern_match.group(1)
    await event.edit("🗄️ Ambil histori URL dari Wayback Machine...")
    try:
        urls = await asyncio.to_thread(_get_wayback_urls, domain)
        if not urls:
            await event.edit("❌ Gak nemu histori URL buat domain ini.")
            return
        text = "\n".join(urls)
        await event.edit(f"🗄️ **{len(urls)} URL historis {domain}:**\n```\n{text}\n```")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
