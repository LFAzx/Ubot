import asyncio
import requests
import xml.etree.ElementTree as ET
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}infonewscyber", "Berita cybersecurity terbaru (CVE, exploit, dll)", "Utility")


def _get_cyber_news():
    resp = requests.get("https://feeds.feedburner.com/TheHackersNews", timeout=15)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    items = root.findall(".//item")[:5]

    results = []
    for item in items:
        title = item.findtext("title", "?")
        link = item.findtext("link", "?")
        results.append((title, link))
    return results


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}infonewscyber$"))
async def infonewscyber_handler(event):
    await event.edit("🛡️ Ambil berita cybersecurity...")
    try:
        news = await asyncio.to_thread(_get_cyber_news)
        if not news:
            await event.edit("❌ Gak ada berita ketemu.")
            return
        lines = [f"- {title}\n  {link}" for title, link in news]
        await event.edit("🛡️ **Berita Cybersecurity Terbaru:**\n" + "\n".join(lines))
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
