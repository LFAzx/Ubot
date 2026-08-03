import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}ip <domain/ip>", "Cek info lokasi IP/domain", "Utility")


def _lookup_ip(target):
    resp = requests.get(f"http://ip-api.com/json/{target}", timeout=10)
    resp.raise_for_status()
    data = resp.json()

    if data.get("status") != "success":
        raise Exception(data.get("message", "Gagal lookup"))

    return (
        f"IP: {data.get('query')}\n"
        f"Negara: {data.get('country')}\n"
        f"Kota: {data.get('city')}\n"
        f"ISP: {data.get('isp')}\n"
        f"Org: {data.get('org')}"
    )


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}ip (\S+)$"))
async def ip_handler(event):
    target = event.pattern_match.group(1)
    await event.edit("🌐 Lookup IP...")
    try:
        result = await asyncio.to_thread(_lookup_ip, target)
        await event.edit(f"🌐 {result}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
