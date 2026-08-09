import os
import re
import asyncio
import tempfile
import yt_dlp
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}getvid <link> [kualitas]", "Download video YT/TikTok (kualitas: 360/480/720/1080)", "Media")
register(f"{PREFIX}getmus <link> [kualitas]", "Download audio dari YT/TikTok (kualitas: 128/192/320)", "Media")

URL_RE = re.compile(r"https?://\S+")
VIDEO_QUALITIES = {"360", "480", "720", "1080"}
AUDIO_QUALITIES = {"128", "192", "320"}


async def _extract_url(event, arg):
    if arg:
        return arg.strip()
    if event.is_reply:
        reply = await event.get_reply_message()
        match = URL_RE.search(reply.raw_text or "")
        if match:
            return match.group(0)
    return None


def _download(url, audio_only=False, quality=None):
    tmpdir = tempfile.mkdtemp()
    outtmpl = os.path.join(tmpdir, "%(title).80s.%(ext)s")

    ydl_opts = {
        "outtmpl": outtmpl,
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }

    if audio_only:
        bitrate = quality if quality in AUDIO_QUALITIES else "192"
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": bitrate,
            }],
        })
    else:
        if quality in VIDEO_QUALITIES:
            fmt = f"bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/best[height<={quality}][ext=mp4]/best"
        else:
            fmt = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
        ydl_opts.update({
            "format": fmt,
            "merge_output_format": "mp4",
        })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filepath = ydl.prepare_filename(info)
        if audio_only:
            filepath = os.path.splitext(filepath)[0] + ".mp3"

    return filepath, info.get("title", "media")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}getvid(?:\s(\S+))?(?:\s(\d+))?$"))
async def getvid_handler(event):
    url = await _extract_url(event, event.pattern_match.group(1))
    quality = event.pattern_match.group(2)

    if not url:
        await event.edit(f"⚠️ Usage: `{PREFIX}getvid <link> [360|480|720|1080]` atau reply pesan yang ada link-nya.")
        return

    label = f" ({quality}p)" if quality else ""
    await event.edit(f"⬇️ Mengunduh video{label}...")
    try:
        filepath, title = await asyncio.to_thread(_download, url, False, quality)
        await event.delete()
        await client.send_file(event.chat_id, filepath, caption=f"🎬 {title}")
        os.remove(filepath)
    except Exception as e:
        await event.edit(f"❌ Error: {e}")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}getmus(?:\s(\S+))?(?:\s(\d+))?$"))
async def getmus_handler(event):
    url = await _extract_url(event, event.pattern_match.group(1))
    quality = event.pattern_match.group(2)

    if not url:
        await event.edit(f"⚠️ Usage: `{PREFIX}getvid <link> [360|480|720|1080]` atau reply pesan yang ada link-nya.")
        return

    label = f" ({quality}p)" if quality else ""
    await event.edit(f"⬇️ Mengunduh video{label}...")
    try:
        filepath, title = await asyncio.to_thread(_download, url, False, quality)
        await event.delete()
        await client.send_file(event.chat_id, filepath, caption=f"🎬 {title}")
        os.remove(filepath)
    except Exception as e:
        await event.edit(f"❌ Error: {e}")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}getmus(?:\s(\S+))?(?:\s(\d+))?$"))
async def getmus_handler(event):
    url = await _extract_url(event, event.pattern_match.group(1))
    quality = event.pattern_match.group(2)

    if not url:
        await event.edit(f"⚠️ Usage: `{PREFIX}getmus <link> [128|192|320]` atau reply pesan yang ada link-nya.")
        return

    label = f" ({quality}kbps)" if quality else ""
    await event.edit(f"⬇️ Mengunduh audio{label}...")
    try:
        filepath, title = await asyncio.to_thread(_download, url, True, quality)
        await event.delete()
        await client.send_file(event.chat_id, filepath, caption=f"🎵 {title}")
        os.remove(filepath)
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
