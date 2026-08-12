import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}paste2text <link>", "Ambil isi teks dari link dpaste/pastebin", "Utility")


def _get_raw_text(url):
    if "dpaste.com" in url and not url.endswith(".txt"):
        url = url.rstrip("/") + ".txt"
    elif "pastebin.com" in url and "/raw/" not in url:
        paste_id = url.rstrip("/").split("/")[-1]
        url = f"https://pastebin.com/raw/{paste_id}"

    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return resp.text


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}paste2text (\S+)$"))
async def paste2text_handler(event):
    link = event.pattern_match.group(1)
    await event.edit("📄 Ambil isi paste...")
    try:
        text = await asyncio.to_thread(_get_raw_text, link)
        text = text[:3500]
        await event.edit(f"📄 **Isi paste:**\n```\n{text}\n```")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
