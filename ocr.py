import io
from telethon import events
from PIL import Image
import pytesseract

from client import client, PREFIX, register

register(f"{PREFIX}ocr", "Extract teks dari foto (reply foto)", "Media")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}ocr$"))
async def ocr_handler(event):
    if not event.is_reply:
        await event.edit("⚠️ Reply ke foto yang mau di-OCR.")
        return

    reply = await event.get_reply_message()
    if not reply.photo:
        await event.edit("⚠️ Pesan yang di-reply harus berupa foto.")
        return

    await event.edit("🔤 Extract teks...")
    try:
        photo_bytes = await client.download_media(reply.photo, file=bytes)
        img = Image.open(io.BytesIO(photo_bytes))
        text = pytesseract.image_to_string(img).strip()

        if not text:
            await event.edit("❌ Gak ada teks yang kedetect di foto ini.")
            return

        await event.edit(f"🔤 **Hasil OCR:**\n\n{text}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
