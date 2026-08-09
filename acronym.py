import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}acronym <singkatan>", "Cari kepanjangan akronim/singkatan", "Utility")


def _lookup_acronym(term):
    resp = requests.get(
        "https://api.duckduckgo.com/",
        params={"q": term, "format": "json", "no_html": 1, "skip_disambig": 1},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    text = data.get("AbstractText") or data.get("Definition")
    if not text:
        raise Exception("Gak nemu kepanjangan buat singkatan ini.")
    return text


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}acronym (.+)$"))
async def acronym_handler(event):
    term = event.pattern_match.group(1)
    await event.edit("🔤 Cari kepanjangan...")
    try:
        result = await asyncio.to_thread(_lookup_acronym, term)
        await event.edit(f"🔤 **{term.upper()}**\n{result}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
