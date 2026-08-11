import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}dnsrecord <domain>", "Lihat DNS records (A, MX, TXT, NS)", "OSINT")

RECORD_TYPES = ["A", "MX", "TXT", "NS"]


def _get_dns_records(domain):
    results = {}
    for rtype in RECORD_TYPES:
        try:
            resp = requests.get(
                "https://cloudflare-dns.com/dns-query",
                params={"name": domain, "type": rtype},
                headers={"Accept": "application/dns-json"},
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            answers = data.get("Answer", [])
            results[rtype] = [a["data"] for a in answers] if answers else []
        except Exception:
            results[rtype] = []
    return results


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}dnsrecord (\S+)$"))
async def dnsrecord_handler(event):
    domain = event.pattern_match.group(1)
    await event.edit("🔎 Lookup DNS records...")
    try:
        records = await asyncio.to_thread(_get_dns_records, domain)
        lines = []
        for rtype, values in records.items():
            if values:
                lines.append(f"**{rtype}:**")
                lines.extend(f"  {v}" for v in values)
            else:
                lines.append(f"**{rtype}:** -")
        await event.edit(f"🔎 **DNS Records: {domain}**\n" + "\n".join(lines))
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
