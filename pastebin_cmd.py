import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}pastebin <teks>", "Simpan teks panjang, dapet link share (dpaste)", "Utility")


def _create_paste(text):
    resp = requests.post(
        "https://dpaste.com/api/v2/",
        data={"content": text, "syntax": "text", "expiry_days": 7},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.text.strip()


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}pastebin ([\s\S]+)$"))
async def pastebin_handler(event):
    text = event.pattern_match.group(1)

    if not text and event.is_reply:
        reply = await event.get_reply_message()
        text = reply.raw_text or ""

    await event.edit("📋 Upload ke dpaste...")
    try:
        url = await asyncio.to_thread(_create_paste, text)
        await event.edit(f"📋 **Link paste (expire 7 hari):**\n{url}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
