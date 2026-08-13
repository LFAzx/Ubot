import socket
import asyncio
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}reversedns <ip>", "Reverse DNS lookup (PTR record)", "OSINT")


def _reverse_dns(ip):
    try:
        hostname, aliases, _ = socket.gethostbyaddr(ip)
        return hostname
    except socket.herror:
        return None


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}reversedns (\S+)$"))
async def reversedns_handler(event):
    ip = event.pattern_match.group(1)
    await event.edit("🔎 Reverse DNS lookup...")
    try:
        hostname = await asyncio.to_thread(_reverse_dns, ip)
        if not hostname:
            await event.edit(f"❌ Gak ada PTR record buat {ip}.")
            return
        await event.edit(f"🔎 **{ip}**\nHostname: {hostname}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
