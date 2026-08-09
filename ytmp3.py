import os
import tempfile
import asyncio
import yt_dlp
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}ytmp3 <judul lagu> <kualitas>", "Cari lagu YouTube, convert MP3 (128/192/320)", "Media")


def _download_mp3(query, quality):
    tmpdir = tempfile.mkdtemp()
    outtmpl = os.path.join(tmpdir, "%(title).80s.%(ext)s")

    ydl_opts = {
        "outtmpl": outtmpl,
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "ignoreerrors": True,
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": quality,
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=True)
        entry = info["entries"][0] if info and "entries" in info else info
        if not entry:
            raise Exception("Lagu gak ditemukan.")
        filepath = ydl.prepare_filename(entry)
        filepath = os.path.splitext(filepath)[0] + ".mp3"

    return filepath, entry.get("title", "audio")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}ytmp3 (.+) (128|192|320)$"))
async def ytmp3_handler(event):
    query = event.pattern_match.group(1)
    quality = event.pattern_match.group(2)

    await event.edit(f"🎵 Cari & convert MP3 ({quality}kbps)...")
    try:
        filepath, title = await asyncio.to_thread(_download_mp3, query, quality)
        await event.delete()
        await client.send_file(event.chat_id, filepath, caption=f"🎵 {title} ({quality}kbps)")
        os.remove(filepath)
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
