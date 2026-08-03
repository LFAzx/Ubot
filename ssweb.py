import io
import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}ssweb <link>", "Screenshot website", "Utility")


def _get_screenshot_bytes(url):
    resp = requests.get(
        "https://api.microlink.io",
        params={"url": url, "screenshot": "true", "meta": "false"},
        timeout=25,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") != "success":
        raise Exception(data.get("message", "Gagal ambil screenshot"))

    shot_url = data["data"]["screenshot"]["url"]
    img_resp = requests.get(shot_url, timeout=25)
    img_resp.raise_for_status()
    return img_resp.content


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}ssweb (\S+)$"))
async def ssweb_handler(event):
    url = event.pattern_match.group(1)
    await event.edit("📸 Screenshot website...")
    try:
        img_bytes = await asyncio.to_thread(_get_screenshot_bytes, url)
        buf = io.BytesIO(img_bytes)
        buf.name = "screenshot.png"

        await event.delete()
        await client.send_file(event.chat_id, buf, caption=f"📸 {url}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
