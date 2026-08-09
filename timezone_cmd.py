import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}timezone <zona>", "Cek jam di zona IANA (misal Asia/Jakarta)", "Utility")


def _get_time(zone):
    resp = requests.get(f"https://worldtimeapi.org/api/timezone/{zone}", timeout=15)
    resp.raise_for_status()
    data = resp.json()
    return data.get("datetime", "?")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}timezone (\S+)$"))
async def timezone_handler(event):
    zone = event.pattern_match.group(1)
    await event.edit("🕐 Cek waktu...")
    try:
        dt = await asyncio.to_thread(_get_time, zone)
        await event.edit(f"🕐 **{zone}**\n{dt}")
    except Exception as e:
        await event.edit(f"❌ Error: {e} (pastikan format zona bener, misal `Asia/Jakarta`)")
