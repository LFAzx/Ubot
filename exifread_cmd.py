import io
from telethon import events
from PIL import Image
from PIL.ExifTags import TAGS

from client import client, PREFIX, register

register(f"{PREFIX}exifread", "Extract metadata EXIF dari foto (reply, kirim sebagai file biar gak ke-strip)", "OSINT")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}exifread$"))
async def exifread_handler(event):
    if not event.is_reply:
        await event.edit("⚠️ Reply ke foto yang mau di-cek metadata-nya.")
        return

    reply = await event.get_reply_message()
    if not (reply.photo or reply.document):
        await event.edit("⚠️ Pesan yang di-reply harus berupa foto/gambar.")
        return

    await event.edit("🔍 Baca metadata EXIF...")
    try:
        photo_bytes = await client.download_media(reply, file=bytes)
        img = Image.open(io.BytesIO(photo_bytes))
        exif_data = img._getexif()

        if not exif_data:
            await event.edit(
                "📭 Gak ada metadata EXIF di foto ini.\n"
                "Kemungkinan Telegram udah strip EXIF-nya (biasa kejadian kalau dikirim sebagai foto biasa, "
                "bukan sebagai file/dokumen)."
            )
            return

        lines = []
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            lines.append(f"**{tag}:** {value}")

        text = "🔍 **EXIF Metadata:**\n" + "\n".join(lines[:20])
        await event.edit(text)
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
