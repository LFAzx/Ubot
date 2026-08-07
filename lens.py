import os
import tempfile
from telethon import events
from playwright.async_api import async_playwright

from client import client, PREFIX, register

register(f"{PREFIX}lens", "Reverse image search (reply foto, cari kecocokan + link sumber)", "Media")

MAX_RESULTS = 5


async def _reverse_search(image_path):
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto("https://yandex.com/images/", timeout=30000)
            await page.wait_for_timeout(2000)

            camera_btn = await page.query_selector(
                "[aria-label='Search by image'], .input__button_camera, [class*='camera']"
            )
            if camera_btn:
                await camera_btn.click()
                await page.wait_for_timeout(1000)

            file_input = await page.query_selector("input[type='file']")
            if not file_input:
                raise Exception("Gak nemu tombol upload gambar di halaman Yandex (struktur halaman mungkin berubah).")

            await file_input.set_input_files(image_path)
            await page.wait_for_timeout(6000)

            links = await page.query_selector_all("a[href^='http']")
            for link in links:
                href = await link.get_attribute("href")
                if href and "yandex" not in href and href not in results:
                    results.append(href)
                if len(results) >= MAX_RESULTS:
                    break
        finally:
            await browser.close()
    return results


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}lens$"))
async def lens_handler(event):
    if not event.is_reply:
        await event.edit("⚠️ Reply ke foto yang mau dicari kecocokannya.")
        return

    reply = await event.get_reply_message()
    if not reply.photo:
        await event.edit("⚠️ Pesan yang di-reply harus berupa foto.")
        return

    await event.edit("🔍 Download foto & cari kecocokan (bisa agak lama)...")
    try:
        photo_bytes = await client.download_media(reply.photo, file=bytes)

        tmpdir = tempfile.mkdtemp()
        image_path = os.path.join(tmpdir, "search.jpg")
        with open(image_path, "wb") as f:
            f.write(photo_bytes)

        results = await _reverse_search(image_path)
        os.remove(image_path)

        if not results:
            await event.edit("❌ Gak nemu hasil (kemungkinan situs pencarian nge-block bot).")
            return

        result_list = "\n".join(f"- {r}" for r in results)
        await event.edit(f"🔍 **Hasil kecocokan gambar:**\n{result_list}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
