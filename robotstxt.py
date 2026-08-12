import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}robotstxt <domain>", "Ambil isi robots.txt suatu domain", "OSINT")


def _get_robots(domain):
    if not domain.startswith(("http://", "https://")):
        domain = "https://" + domain
    domain = domain.rstrip("/")
    resp = requests.get(f"{domain}/robots.txt", timeout=15)
    resp.raise_for_status()
    return resp.text


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}robotstxt (\S+)$"))
async def robotstxt_handler(event):
    domain = event.pattern_match.group(1)
    await event.edit("🤖 Ambil robots.txt...")
    try:
        text = await asyncio.to_thread(_get_robots, domain)
        text = text[:3500]
        if not text.strip():
            await event.edit("📭 robots.txt kosong.")
            return
        await event.edit(f"🤖 **robots.txt {domain}:**\n```\n{text}\n```")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
