import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}whois <domain>", "Cek info domain (registrar, tanggal daftar/expire)", "Utility")


def _whois_lookup(domain):
    resp = requests.get(f"https://rdap.org/domain/{domain}", timeout=15)
    resp.raise_for_status()
    data = resp.json()

    events_list = data.get("events", [])
    reg_date = next((e["eventDate"] for e in events_list if e["eventAction"] == "registration"), "?")
    exp_date = next((e["eventDate"] for e in events_list if e["eventAction"] == "expiration"), "?")

    registrar = "?"
    for entity in data.get("entities", []):
        if "registrar" in entity.get("roles", []):
            vcard = entity.get("vcardArray")
            if vcard and len(vcard) > 1:
                for item in vcard[1]:
                    if item[0] == "fn":
                        registrar = item[3]

    name = data.get("ldhName", domain)
    return f"**Domain:** {name}\n**Registered:** {reg_date}\n**Expires:** {exp_date}\n**Registrar:** {registrar}"


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}whois (\S+)$"))
async def whois_handler(event):
    domain = event.pattern_match.group(1)
    await event.edit("🔎 Cari info domain...")
    try:
        result = await asyncio.to_thread(_whois_lookup, domain)
        await event.edit(f"🔎 {result}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
