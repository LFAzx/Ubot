import asyncio
import requests
from datetime import datetime, timezone
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}domainage <domain>", "Cek umur domain (tanggal registrasi)", "OSINT")


def _get_domain_age(domain):
    resp = requests.get(f"https://rdap.org/domain/{domain}", timeout=15)
    resp.raise_for_status()
    data = resp.json()

    events_list = data.get("events", [])
    reg_date_str = next((e["eventDate"] for e in events_list if e["eventAction"] == "registration"), None)
    if not reg_date_str:
        raise Exception("Tanggal registrasi gak ketemu buat domain ini.")

    reg_date = datetime.fromisoformat(reg_date_str.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    age_days = (now - reg_date).days
    age_years = age_days // 365

    return reg_date, age_years, age_days


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}domainage (\S+)$"))
async def domainage_handler(event):
    domain = event.pattern_match.group(1)
    await event.edit("📅 Cek umur domain...")
    try:
        reg_date, age_years, age_days = await asyncio.to_thread(_get_domain_age, domain)
        await event.edit(
            f"📅 **{domain}**\n"
            f"Terdaftar: {reg_date.strftime('%Y-%m-%d')}\n"
            f"Umur: ~{age_years} tahun ({age_days:,} hari)"
        )
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
