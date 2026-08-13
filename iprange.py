import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}iprange <ip>", "Cek CIDR/network range suatu IP (RDAP)", "OSINT")


def _get_ip_range(ip):
    resp = requests.get(f"https://rdap.org/ip/{ip}", timeout=15)
    resp.raise_for_status()
    data = resp.json()

    cidr = None
    for cidr_entry in data.get("cidr0_cidrs", []):
        prefix = cidr_entry.get("v4prefix") or cidr_entry.get("v6prefix")
        length = cidr_entry.get("length")
        if prefix and length is not None:
            cidr = f"{prefix}/{length}"
            break

    return {"cidr": cidr or "?", "name": data.get("name", "?"), "handle": data.get("handle", "?")}


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}iprange (\S+)$"))
async def iprange_handler(event):
    ip = event.pattern_match.group(1)
    await event.edit("🌐 Cek network range...")
    try:
        info = await asyncio.to_thread(_get_ip_range, ip)
        text = (
            f"🌐 **{ip}**\n"
            f"CIDR: {info['cidr']}\n"
            f"Nama block: {info['name']}\n"
            f"Handle: {info['handle']}"
        )
        await event.edit(text)
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
