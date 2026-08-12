import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}geoip <ip>", "Lokasi geografis dari IP address", "OSINT")


def _geoip_lookup(ip):
    resp = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") != "success":
        raise Exception(data.get("message", "Gagal lookup"))
    return data


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}geoip (\S+)$"))
async def geoip_handler(event):
    ip = event.pattern_match.group(1)
    await event.edit("🌍 Lookup lokasi IP...")
    try:
        data = await asyncio.to_thread(_geoip_lookup, ip)
        text = (
            f"🌍 **{data.get('query')}**\n"
            f"Negara: {data.get('country')}\n"
            f"Region: {data.get('regionName')}\n"
            f"Kota: {data.get('city')}\n"
            f"Koordinat: {data.get('lat')}, {data.get('lon')}\n"
            f"ISP: {data.get('isp')}"
        )
        await event.edit(text)
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
