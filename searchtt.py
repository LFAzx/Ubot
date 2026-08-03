import os
import asyncio
from urllib.parse import quote_plus
from playwright.async_api import async_playwright
from telethon import events

from client import client, PREFIX, register
from media import _download

register(f"{PREFIX}searchtt <kata kunci> <jumlah>", "Cari & download video TikTok (browser headless)", "Media")

MAX_RESULTS = 5


async def _search_tiktok_urls(query, count):
    urls = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(f"https://www.tiktok.com/search/video?q={quote_plus(query)}", timeout=30000)
            await page.wait_for_timeout(4000)

            anchors = await page.query_selector_all("a[href*='/video/']")
            for a in anchors:
                href = await a.get_attribute("href")
                if href and href not in urls:
                    urls.append(href)
                if len(urls) >= count:
                    break
        finally:
            await browser.close()
    return urls[:count]


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}searchtt (.+) (\d+)$"))
async def searchtt_handler(event):
    query = event.pattern_match.group(1)
    count = min(int(event.pattern_match.group(2)), MAX_RESULTS)

    await event.edit(f"🔎 Mencari TikTok: {query}...")
    try:
        urls = await _search_tiktok_urls(query, count)
        if not urls:
            await event.edit("❌ Gak nemu hasil (TikTok mungkin lagi block bot detection).")
            return

        await event.edit(f"⬇️ Ketemu {len(urls)}, mulai download...")

        uploaders = []
        filepaths = []
        for url in urls:
            try:
                filepath, title = await asyncio.to_thread(_download, url, False)
                filepaths.append(filepath)
                uploaders.append(url.split("@")[1].split("/")[0] if "@" in url else "?")
            except Exception:
                continue

        if not filepaths:
            await event.edit("❌ Gagal download semua hasil.")
            return

        await event.delete()
        for fp in filepaths:
            await client.send_file(event.chat_id, fp)
            os.remove(fp)

        uploader_list = "\n".join(f"- @{u}" for u in uploaders)
        await client.send_message(event.chat_id, f"📃 **List user:**\n{uploader_list}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
