import io
import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}freeproxy <jumlah> <text|file>", "List proxy gratisan (HTTP)", "Utility")


def _fetch_proxies(count):
    resp = requests.get("https://www.proxy-list.download/api/v1/get?type=http", timeout=15)
    resp.raise_for_status()
    lines = [l.strip() for l in resp.text.splitlines() if l.strip()]
    return lines[:count]


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}freeproxy (\d+) (text|file)$"))
async def freeproxy_handler(event):
    count = int(event.pattern_match.group(1))
    fmt = event.pattern_match.group(2)

    await event.edit("🌐 Ambil list proxy...")
    try:
        proxies = await asyncio.to_thread(_fetch_proxies, count)
        if not proxies:
            await event.edit("❌ Gak ada proxy yang kedapet.")
            return

        if fmt == "file":
            buf = io.BytesIO("\n".join(proxies).encode())
            buf.name = "proxies.txt"
            await event.delete()
            await client.send_file(event.chat_id, buf, caption=f"🌐 {len(proxies)} proxy (HTTP)")
        else:
            text = "\n".join(proxies)
            await event.edit(f"🌐 **{len(proxies)} Proxy (HTTP):**\n```\n{text}\n```")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
