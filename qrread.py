import io
from telethon import events
from PIL import Image
from pyzbar.pyzbar import decode

from client import client, PREFIX, register

register(f"{PREFIX}qrread", "Baca isi QR code dari foto (reply foto)", "Media")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}qrread$"))
async def qrread_handler(event):
    if not event.is_reply:
        await event.edit("⚠️ Reply ke foto QR code.")
        return

    reply = await event.get_reply_message()
    if not reply.photo:
        await event.edit("⚠️ Pesan yang di-reply harus berupa foto.")
        return

    await event.edit("🔍 Baca QR code...")
    try:
        photo_bytes = await client.download_media(reply.photo, file=bytes)
        img = Image.open(io.BytesIO(photo_bytes))
        results = decode(img)

        if not results:
            await event.edit("❌ Gak ada QR code yang kedetect.")
            return

        text = "\n".join(r.data.decode("utf-8", errors="replace") for r in results)
        await event.edit(f"🔍 **Isi QR:**\n{text}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
