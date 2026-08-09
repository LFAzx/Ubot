import asyncio
import time
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}ping2 <domain>", "Cek website up atau down", "Utility")


def _check_site(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    start = time.time()
    resp = requests.get(url, timeout=10)
    elapsed = (time.time() - start) * 1000
    return resp.status_code, elapsed


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}ping2 (\S+)$"))
async def ping2_handler(event):
    url = event.pattern_match.group(1)
    await event.edit("🌐 Cek status website...")
    try:
        status, ms = await asyncio.to_thread(_check_site, url)
        emoji = "🟢" if status < 400 else "🔴"
        await event.edit(f"{emoji} **{url}**\nStatus: {status}\nResponse time: {ms:.0f}ms")
    except Exception as e:
        await event.edit(f"🔴 **{url}** kemungkinan down.\nError: {e}")
