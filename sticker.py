import io
from telethon import events
from telethon.tl.types import DocumentAttributeFilename
from PIL import Image

from client import client, PREFIX, register

register(f"{PREFIX}sticker", "Reply foto untuk dijadikan stiker", "Media")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}sticker$"))
async def sticker_handler(event):
    if not event.is_reply:
        await event.edit("⚠️ Reply ke sebuah foto dulu.")
        return

    reply = await event.get_reply_message()
    if not reply.photo:
        await event.edit("⚠️ Pesan yang di-reply harus berupa foto.")
        return

    await event.edit("🖼️ Membuat stiker...")
    try:
        photo_bytes = await client.download_media(reply.photo, file=bytes)
        img = Image.open(io.BytesIO(photo_bytes)).convert("RGBA")
        img.thumbnail((512, 512))

        buf = io.BytesIO()
        buf.name = "sticker.webp"
        img.save(buf, "WEBP")
        buf.seek(0)

        await event.delete()
        await client.send_file(
            event.chat_id,
            buf,
            attributes=[DocumentAttributeFilename("sticker.webp")],
            force_document=False,
        )
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
