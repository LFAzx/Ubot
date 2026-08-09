import io
import asyncio
import requests
from telethon import events
from pinscrape import Pinterest

from client import client, PREFIX, register

register(f"{PREFIX}searchpin <teks> <jumlah>", "Cari & download foto dari Pinterest", "Media")

MAX_RESULTS = 10


def _search_and_download(keyword, count):
    p = Pinterest()
    urls = p.search(keyword, count)

    files = []
    for u in urls[:count]:
        try:
            img_resp = requests.get(u, timeout=15)
            img_resp.raise_for_status()
            buf = io.BytesIO(img_resp.content)
            buf.name = "pin.jpg"
            files.append(buf)
        except Exception:
            continue

    return files


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}searchpin (.+) (\d+)$"))
async def searchpin_handler(event):
    keyword = event.pattern_match.group(1)
    count = min(int(event.pattern_match.group(2)), MAX_RESULTS)

    await event.edit("📌 Mencari & download dari Pinterest...")
    try:
        files = await asyncio.to_thread(_search_and_download, keyword, count)

        if not files:
            await event.edit("❌ Gak nemu atau gagal download hasil pencarian.")
            return

        await event.delete()
        await client.send_file(event.chat_id, files, caption=f"📌 Hasil pencarian: {keyword}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
