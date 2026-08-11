import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}usernamecheck <username>", "Cek ketersediaan username di berbagai platform", "OSINT")

PLATFORMS = {
    "GitHub": "https://github.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "X (Twitter)": "https://x.com/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Telegram": "https://t.me/{}",
}


def _check_username(username):
    results = {}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    for platform, url_template in PLATFORMS.items():
        url = url_template.format(username)
        try:
            resp = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            exists = resp.status_code == 200
        except Exception:
            exists = None
        results[platform] = exists
    return results


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}usernamecheck (\S+)$"))
async def usernamecheck_handler(event):
    username = event.pattern_match.group(1)
    await event.edit("🔎 Cek username di berbagai platform...")
    try:
        results = await asyncio.to_thread(_check_username, username)
        lines = []
        for platform, exists in results.items():
            if exists is True:
                lines.append(f"✅ {platform}")
            elif exists is False:
                lines.append(f"❌ {platform}")
            else:
                lines.append(f"❓ {platform} (gak bisa dicek)")
        await event.edit(f"🔎 **Username: {username}**\n" + "\n".join(lines))
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
