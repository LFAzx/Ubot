import asyncio
import yt_dlp
from telethon import events

from client import client, PREFIX, register
from yt_cookies import get_youtube_cookiefile

register(f"{PREFIX}infouseryt <nama channel/link>", "Info channel YouTube (subscriber, dll)", "Utility")


def _get_channel_info(query):
    target = query if query.startswith("http") else f"ytsearch1:{query}"

    base_opts = {"quiet": True, "no_warnings": True}
    cookiefile = get_youtube_cookiefile()
    if cookiefile:
        base_opts["cookiefile"] = cookiefile

    with yt_dlp.YoutubeDL({**base_opts, "extract_flat": True}) as ydl:
        info = ydl.extract_info(target, download=False)
        entry = info["entries"][0] if info and "entries" in info else info
        if not entry:
            raise Exception("Channel/video gak ditemukan.")
        video_url = entry.get("url") or entry.get("webpage_url") or f"https://www.youtube.com/watch?v={entry.get('id')}"

    with yt_dlp.YoutubeDL(base_opts) as ydl:
        full_info = ydl.extract_info(video_url, download=False)

    return {
        "channel": full_info.get("channel") or full_info.get("uploader"),
        "channel_url": full_info.get("channel_url") or full_info.get("uploader_url"),
        "subscribers": full_info.get("channel_follower_count"),
    }


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}infouseryt (.+)$"))
async def infouseryt_handler(event):
    query = event.pattern_match.group(1)
    await event.edit("🔎 Cari info channel YouTube...")
    try:
        info = await asyncio.to_thread(_get_channel_info, query)
        subs = f"{info['subscribers']:,}" if info.get("subscribers") else "?"
        text = f"**📺 {info['channel']}**\nSubscribers: {subs}\n{info['channel_url']}"
        await event.edit(text)
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
