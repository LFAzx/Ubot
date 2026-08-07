import os
import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}lens <jumlah> <google|yandex|all>", "Reverse image search via SerpApi (reply foto)", "Media")

MAX_RESULTS = 10
SERPAPI_KEY = os.environ.get("SERPAPI_KEY")


def _upload_temp_image(image_bytes):
    resp = requests.post(
        "https://catbox.moe/user/api.php",
        data={"reqtype": "fileupload"},
        files={"fileToUpload": ("search.jpg", image_bytes)},
        timeout=30,
    )
    resp.raise_for_status()
    url = resp.text.strip()
    if not url.startswith("http"):
        raise Exception("Gagal upload gambar sementara buat pencarian.")
    return url


def _search_google_lens(image_url, count):
    resp = requests.get(
        "https://serpapi.com/search",
        params={"engine": "google_lens", "url": image_url, "api_key": SERPAPI_KEY},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    matches = data.get("visual_matches", [])
    results = []
    for m in matches[:count]:
        link = m.get("link")
        if link:
            results.append(("Google", link))
    return results


def _search_yandex_images(image_url, count):
    resp = requests.get(
        "https://serpapi.com/search",
        params={"engine": "yandex_images", "url": image_url, "api_key": SERPAPI_KEY},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    matches = data.get("similar_images") or data.get("image_results") or []
    results = []
    for m in matches[:count]:
        link = m.get("link") or m.get("source")
        if link:
            results.append(("Yandex", link))
    return results


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}lens (\d+) (google|yandex|all)$"))
async def lens_handler(event):
    if not SERPAPI_KEY:
        await event.edit("⚠️ SERPAPI_KEY belum di-set di environment variable Railway.")
        return

    if not event.is_reply:
        await event.edit("⚠️ Reply ke foto yang mau dicari kecocokannya.")
        return

    reply = await event.get_reply_message()
    if not reply.photo:
        await event.edit("⚠️ Pesan yang di-reply harus berupa foto.")
        return

    count = min(int(event.pattern_match.group(1)), MAX_RESULTS)
    platform = event.pattern_match.group(2)

    await event.edit("🔍 Upload & cari kecocokan gambar...")
    try:
        photo_bytes = await client.download_media(reply.photo, file=bytes)
        image_url = await asyncio.to_thread(_upload_temp_image, photo_bytes)

        results = []
        if platform in ("google", "all"):
            results += await asyncio.to_thread(_search_google_lens, image_url, count)
        if platform in ("yandex", "all"):
            results += await asyncio.to_thread(_search_yandex_images, image_url, count)

        results = results[:count]

        if not results:
            await event.edit("❌ Gak nemu hasil kecocokan.")
            return

        result_list = "\n".join(f"[{src}] {link}" for src, link in results)
        await event.edit(f"🔍 **Hasil kecocokan gambar:**\n{result_list}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
