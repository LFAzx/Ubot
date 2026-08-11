import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}subdomain <domain>", "Enumerasi subdomain (Certificate Transparency logs)", "OSINT")


def _get_subdomains(domain):
    resp = requests.get(f"https://crt.sh/?q=%25.{domain}&output=json", timeout=20)
    resp.raise_for_status()
    data = resp.json()
    subdomains = set()
    for entry in data:
        name = entry.get("name_value", "")
        for sub in name.split("\n"):
            if domain in sub:
                subdomains.add(sub.strip())
    return sorted(subdomains)


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}subdomain (\S+)$"))
async def subdomain_handler(event):
    domain = event.pattern_match.group(1)
    await event.edit("🔎 Enumerasi subdomain...")
    try:
        subs = await asyncio.to_thread(_get_subdomains, domain)
        if not subs:
            await event.edit("❌ Gak nemu subdomain.")
            return
        text = "\n".join(subs[:40])
        await event.edit(f"🔎 **Subdomain {domain}** ({len(subs)} ditemukan):\n```\n{text}\n```")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
