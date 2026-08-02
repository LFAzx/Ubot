import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}weather <kota>", "Cek cuaca (data dari wttr.in)", "Utility")


def _fetch_weather(city):
    resp = requests.get(f"https://wttr.in/{city}", params={"format": "3"}, timeout=10)
    resp.raise_for_status()
    return resp.text.strip()


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}weather (.+)$"))
async def weather_handler(event):
    city = event.pattern_match.group(1)
    await event.edit("🌤️ Cek cuaca...")
    try:
        result = await asyncio.to_thread(_fetch_weather, city)
        await event.edit(f"🌤️ {result}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
