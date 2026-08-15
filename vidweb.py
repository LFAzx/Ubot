import os
import subprocess
import asyncio
from playwright.async_api import async_playwright
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}vidweb <link> <durasi>", "Rekam video scroll halaman web jadi MP4 (durasi detik, maks 20)", "Media")

MAX_DURATION = 20


async def _record_scroll(url, duration):
    video_dir = "/tmp/vidweb"
    os.makedirs(video_dir, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 800, "height": 600},
            record_video_dir=video_dir,
            record_video_size={"width": 800, "height": 600},
        )
        page = await context.new_page()
        await page.goto(url, timeout=30000)
        await page.wait_for_timeout(1500)

        steps = max(int(duration / 0.5), 1)
        for _ in range(steps):
            await page.mouse.wheel(0, 400)
            await page.wait_for_timeout(500)

        video = page.video
        await context.close()
        await browser.close()

        return await video.path()


def _convert_to_mp4(webm_path):
    mp4_path = webm_path.rsplit(".", 1)[0] + ".mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-i", webm_path, "-c:v", "libx264", "-pix_fmt", "yuv420p", mp4_path],
        check=True,
        capture_output=True,
    )
    os.remove(webm_path)
    return mp4_path


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}vidweb (\S+) (\d+)$"))
async def vidweb_handler(event):
    url = event.pattern_match.group(1)
    duration = min(int(event.pattern_match.group(2)), MAX_DURATION)

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    await event.edit(f"🎥 Rekam video scroll ({duration} detik)...")
    try:
        webm_path = await _record_scroll(url, duration)

        await event.edit("🎥 Convert ke MP4...")
        mp4_path = await asyncio.to_thread(_convert_to_mp4, webm_path)

        await event.delete()
        await client.send_file(event.chat_id, mp4_path, caption=f"🎥 {url}")
        os.remove(mp4_path)
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
