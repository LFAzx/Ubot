import os
import tempfile
from urllib.parse import urlparse, parse_qs, unquote
from telethon import events
from playwright.async_api import async_playwright

from client import client, PREFIX, register

register(f"{PREFIX}lens <jumlah>", "Reverse image search via Yandex (reply foto)", "Media")

MAX_RESULTS = 10


def _extract_yandex_img_url(href):
    parsed = urlparse(href)
    qs = parse_qs(parsed.query)
    if "img_url" in qs:
        return unquote(qs["img_url"][0])
    return href


async def _search_yandex(image_path, count):
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
                return results

            await file_input.set_input_files(image_path)
            await page.wait_for_timeout(6000)

            anchors = await page.query_selector_all("a[href*='cbir_id']")
            seen = set()
            for a in anchors:
                href = await a.get_attribute("href")
                if not href:
                    continue
                img_url = _extract_yandex_img_url(href)
                if img_url not in seen:
                    seen.add(img_url)
                    results.append(img_url)
                if len(results) >= count:
                    break
        except Exception:
            pass
        finally:
            await browser.close()
    return results


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}lens (\d+)$"))
async def lens_handler(event):
    if not event.is_reply:
        await event.edit("⚠️ Reply ke foto yang mau dicari kecocokannya.")
        return

    reply = await event.get_reply_message()
    if not reply.photo:
        await event.edit("⚠️ Pesan yang di-reply harus berupa foto.")
        return

    count = min(int(event.pattern_match.group(1)), MAX_RESULTS)

    await event.edit("🔍 Cari kecocokan gambar di Yandex...")
    try:
        photo_bytes = await client.download_media(reply.photo, file=bytes)

        tmpdir = tempfile.mkdtemp()
        image_path = os.path.join(tmpdir, "search.jpg")
        with open(image_path, "wb") as f:
            f.write(photo_bytes)

        results = await _search_yandex(image_path, count)
        os.remove(image_path)

        if not results:
            await event.edit("❌ Gak nemu hasil (kemungkinan situs pencarian nge-block bot dari server).")
            return

        result_list = "\n".join(f"- {r}" for r in results)
        await event.edit(f"🔍 **Hasil kecocokan gambar:**\n{result_list}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
