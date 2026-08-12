import re
import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}metatags <url>", "Ambil title, meta description, generator dari suatu halaman", "OSINT")


def _get_meta(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    resp.raise_for_status()
    html = resp.text

    title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
    generator_match = re.search(r'<meta\s+name=["\']generator["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)

    return {
        "title": title_match.group(1).strip() if title_match else "-",
        "description": desc_match.group(1).strip() if desc_match else "-",
        "generator": generator_match.group(1).strip() if generator_match else "-",
    }


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}metatags (\S+)$"))
async def metatags_handler(event):
    url = event.pattern_match.group(1)
    await event.edit("🔎 Ambil meta tags...")
    try:
        meta = await asyncio.to_thread(_get_meta, url)
        text = (
            f"🔎 **{url}**\n"
            f"Title: {meta['title']}\n"
            f"Description: {meta['description']}\n"
            f"Generator/CMS: {meta['generator']}"
        )
        await event.edit(text)
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
