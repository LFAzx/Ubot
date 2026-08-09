import os
import asyncio
import yt_dlp
from telethon import events

from client import client, PREFIX, register
from media import _download

register(f"{PREFIX}searchyt <kata kunci> <jumlah> <shorts|video>", "Cari & download video/shorts YouTube", "Media")

MAX_RESULTS = 5


def _search_youtube(query, count, mode):
    multiplier = 6 if mode == "shorts" else 3
    fetch_count = max(count * multiplier, count + 5)

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "ignoreerrors": True,
        "extract_flat": False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch{fetch_count}:{query}", download=False)
        entries = info.get("entries", []) or []

    filtered = []
    for entry in entries:
        if not entry:
            continue
        duration = entry.get("duration") or 0
        is_short = 0 < duration <= 60
        if mode == "shorts" and is_short:
            filtered.append(entry)
        elif mode == "video" and not is_short:
            filtered.append(entry)
        if len(filtered) >= count:
            break

    return filtered[:count]


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}searchyt (.+) (\d+) (shorts|video)$"))
async def searchyt_handler(event):
    query = event.pattern_match.group(1)
    count = min(int(event.pattern_match.group(2)), MAX_RESULTS)
    mode = event.pattern_match.group(3)

    await event.edit(f"🔎 Mencari {mode} YouTube: {query}...")
    try:
        entries = await asyncio.to_thread(_search_youtube, query, count, mode)
        if not entries:
            await event.edit("❌ Gak nemu hasil yang cocok.")
            return

        await event.edit(f"⬇️ Ketemu {len(entries)}, mulai download...")

        uploaders = []
        filepaths = []
        for entry in entries:
            url = entry.get("webpage_url") or f"https://www.youtube.com/watch?v={entry.get('id')}"
            try:
                filepath, title = await asyncio.to_thread(_download, url, False)
                filepaths.append(filepath)
                uploaders.append(entry.get("uploader") or entry.get("channel") or "?")
            except Exception:
                continue

        if not filepaths:
            await event.edit("❌ Gagal download semua hasil.")
            return

        await event.delete()

        for fp in filepaths:
            await client.send_file(event.chat_id, fp)
            os.remove(fp)

        uploader_list = "\n".join(f"- {u}" for u in uploaders)
        await client.send_message(event.chat_id, f"📃 **List channel:**\n{uploader_list}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
