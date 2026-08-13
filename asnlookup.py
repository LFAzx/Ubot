import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}asnlookup <asn>", "Info detail ASN (nama, negara, deskripsi)", "OSINT")


def _lookup_asn(asn):
    asn_num = asn.upper().replace("AS", "")
    resp = requests.get(f"https://api.bgpview.io/asn/{asn_num}", timeout=15)
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") != "ok":
        raise Exception("ASN gak ditemukan.")
    return data.get("data", {})


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}asnlookup (\S+)$"))
async def asnlookup_handler(event):
    asn = event.pattern_match.group(1)
    await event.edit("🔎 Lookup ASN...")
    try:
        info = await asyncio.to_thread(_lookup_asn, asn)
        text = (
            f"🔎 **AS{info.get('asn')}**\n"
            f"Nama: {info.get('name')}\n"
            f"Deskripsi: {info.get('description_short')}\n"
            f"Negara: {info.get('country_code')}\n"
            f"Website: {info.get('website') or '-'}"
        )
        await event.edit(text)
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
