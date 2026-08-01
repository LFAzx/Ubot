import os
import re
import asyncio
import tempfile
import yt_dlp
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}getvid <link>", "Download video YT/TikTok (reply link juga bisa)", "Media")
register(f"{PREFIX}getmus <link>", "Download audio dari YT/TikTok (reply link juga bisa)", "Media")

URL_RE = re.compile(r"https?://\S+")


async def _extract_url(event, arg):
    if arg:
        return arg.strip()
    if event.is_reply:
        reply = await event.get_reply_message()
        match = URL_RE.search(reply.raw_text or "")
        if match:
            return match.group(0)
    return None


def _download(url, audio_only=False):
    tmpdir = tempfile.mkdtemp()
    outtmpl = os.path.join(tmpdir, "%(title).80s.%(ext)s")

    ydl_opts = {
        "outtmpl": outtmpl,
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }

    if audio_only:
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })
    else:
        ydl_opts.update({
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "merge_output_format": "mp4",
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filepath = ydl.prepare_filename(info)
        if audio_only:
            filepath = os.path.splitext(filepath)[0] + ".mp3"

    return filepath, info.get("title", "media")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}getvid(?:\s(\S+))?$"))
async def getvid_handler(event):
    url = await _extract_url(event, event.pattern_match.group(1))
    if not url:
        await event.edit(f"⚠️ Usage: `{PREFIX}getvid <link>` atau reply pesan yang ada link-nya.")
        return

    await event.edit("⬇️ Mengunduh video...")
    try:
        filepath, title = await asyncio.to_thread(_download, url, False)
        await event.delete()
        await client.send_file(event.chat_id, filepath, caption=f"🎬 {title}")
        os.remove(filepath)
    except Exception as e:
        await event.edit(f"❌ Error: {e}")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}getmus(?:\s(\S+))?$"))
async def getmus_handler(event):
    url = await _extract_url(event, event.pattern_match.group(1))
    if not url:
        await event.edit(f"⚠️ Usage: `{PREFIX}getmus <link>` atau reply pesan yang ada link-nya.")
        return

    await event.edit("⬇️ Mengunduh audio...")
    try:
        filepath, title = await asyncio.to_thread(_download, url, True)
        await event.delete()
        await client.send_file(event.chat_id, filepath, caption=f"🎵 {title}")
        os.remove(filepath)
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
