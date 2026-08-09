import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}holiday <kode_negara>", "Cek hari libur nasional terdekat (misal ID, US, JP)", "Utility")


def _get_holidays(country_code):
    resp = requests.get(f"https://date.nager.at/api/v3/NextPublicHolidays/{country_code.upper()}", timeout=15)
    resp.raise_for_status()
    data = resp.json()
    if not data:
        raise Exception("Gak ada data libur buat kode negara ini.")
    return data[:5]


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}holiday (\S+)$"))
async def holiday_handler(event):
    country = event.pattern_match.group(1)
    await event.edit("📅 Cek hari libur...")
    try:
        holidays = await asyncio.to_thread(_get_holidays, country)
        lines = [f"- {h['date']}: {h['localName']}" for h in holidays]
        await event.edit(f"📅 **Libur nasional {country.upper()}:**\n" + "\n".join(lines))
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
