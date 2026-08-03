import io
import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}meme", "Meme random dari Reddit", "Fun")


def _fetch_meme():
    resp = requests.get("https://meme-api.com/gimme", timeout=15)
    resp.raise_for_status()
    data = resp.json()

    img_resp = requests.get(data["url"], timeout=15)
    img_resp.raise_for_status()
    return img_resp.content, data.get("title", "meme")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}meme$"))
async def meme_handler(event):
    await event.edit("😹 Cari meme...")
    try:
        img_bytes, title = await asyncio.to_thread(_fetch_meme)
        buf = io.BytesIO(img_bytes)
        buf.name = "meme.jpg"

        await event.delete()
        await client.send_file(event.chat_id, buf, caption=title)
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
