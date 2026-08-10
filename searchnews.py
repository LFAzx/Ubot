import asyncio
import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}searchnews <teks>", "Cari berita dari Google News", "Utility")


def _search_news(query):
    url = f"https://news.google.com/rss/search?q={quote(query)}"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    items = root.findall(".//item")[:5]

    results = []
    for item in items:
        title = item.findtext("title", "?")
        link = item.findtext("link", "?")
        results.append((title, link))
    return results


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}searchnews (.+)$"))
async def searchnews_handler(event):
    query = event.pattern_match.group(1)
    await event.edit("📰 Cari berita...")
    try:
        news = await asyncio.to_thread(_search_news, query)
        if not news:
            await event.edit("❌ Gak nemu berita.")
            return
        lines = [f"- {title}\n  {link}" for title, link in news]
        await event.edit(f"📰 **Berita: {query}**\n" + "\n".join(lines))
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
