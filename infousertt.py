import re
import json
import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}infousertt <username>", "Info akun TikTok (followers, bio, video count)", "Utility")


def _get_tiktok_info(username):
    username = username.lstrip("@")
    url = f"https://www.tiktok.com/@{username}"
    resp = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0.0.0"},
        timeout=20,
    )
    resp.raise_for_status()

    match = re.search(r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>', resp.text)
    if not match:
        raise Exception("Gak nemu data user (kemungkinan TikTok ubah struktur halaman atau blokir request).")

    data = json.loads(match.group(1))
    user_info = data["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]
    user = user_info["user"]
    stats = user_info["stats"]

    return {
        "nickname": user.get("nickname"),
        "username": user.get("uniqueId"),
        "bio": user.get("signature") or "-",
        "followers": stats.get("followerCount", 0),
        "following": stats.get("followingCount", 0),
        "likes": stats.get("heartCount", 0),
        "videos": stats.get("videoCount", 0),
        "url": url,
    }


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}infousertt (\S+)$"))
async def infousertt_handler(event):
    username = event.pattern_match.group(1)
    await event.edit("🔎 Cari info akun TikTok...")
    try:
        info = await asyncio.to_thread(_get_tiktok_info, username)
        text = (
            f"**🎵 {info['nickname']}** (@{info['username']})\n"
            f"Followers: {info['followers']:,}\n"
            f"Following: {info['following']:,}\n"
            f"Likes: {info['likes']:,}\n"
            f"Videos: {info['videos']:,}\n"
            f"Bio: {info['bio']}\n"
            f"{info['url']}"
        )
        await event.edit(text)
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
