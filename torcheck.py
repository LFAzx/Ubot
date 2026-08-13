import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}torcheck <ip>", "Cek apakah IP adalah Tor exit node", "OSINT")


def _check_tor(ip):
    resp = requests.get("https://check.torproject.org/torbulkexitlist", timeout=15)
    resp.raise_for_status()
    exit_nodes = set(resp.text.splitlines())
    return ip in exit_nodes


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}torcheck (\S+)$"))
async def torcheck_handler(event):
    ip = event.pattern_match.group(1)
    await event.edit("🧅 Cek Tor exit node list...")
    try:
        is_tor = await asyncio.to_thread(_check_tor, ip)
        if is_tor:
            await event.edit(f"🧅 **{ip}**\n✅ TERDAFTAR sebagai Tor exit node.")
        else:
            await event.edit(f"🧅 **{ip}**\n❌ Bukan Tor exit node (tercatat saat ini).")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
