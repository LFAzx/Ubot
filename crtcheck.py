import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}crtcheck <domain>", "Histori sertifikat SSL yang pernah diterbitkan (crt.sh)", "OSINT")


def _get_cert_history(domain):
    resp = requests.get(f"https://crt.sh/?q={domain}&output=json", timeout=20)
    resp.raise_for_status()
    data = resp.json()

    seen = set()
    entries = []
    for entry in data:
        cert_id = entry.get("id")
        if cert_id in seen:
            continue
        seen.add(cert_id)
        entries.append(entry)

    entries.sort(key=lambda e: e.get("entry_timestamp", ""), reverse=True)
    return entries[:10]


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}crtcheck (\S+)$"))
async def crtcheck_handler(event):
    domain = event.pattern_match.group(1)
    await event.edit("🔎 Ambil histori sertifikat...")
    try:
        entries = await asyncio.to_thread(_get_cert_history, domain)
        if not entries:
            await event.edit("❌ Gak nemu histori sertifikat.")
            return

        lines = []
        for e in entries:
            cn = e.get("common_name", "?")
            issuer = e.get("issuer_name", "?").split(",")[0]
            not_before = (e.get("not_before") or "?")[:10]
            lines.append(f"- {cn} | {issuer} | {not_before}")

        await event.edit(f"🔎 **Histori sertifikat {domain}** ({len(entries)} terbaru):\n" + "\n".join(lines))
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
