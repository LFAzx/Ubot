import io
from telethon import events
from PIL import Image, ImageEnhance, ImageFilter

from client import client, PREFIX, register

register(f"{PREFIX}upscale <scale>", "Perbesar & pertajam foto (2/3/4x, reply foto)", "Media")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}upscale (\d+)$"))
async def upscale_handler(event):
    scale = min(int(event.pattern_match.group(1)), 4)

    if not event.is_reply:
        await event.edit("⚠️ Reply ke foto yang mau di-upscale.")
        return

    reply = await event.get_reply_message()
    if not reply.photo:
        await event.edit("⚠️ Pesan yang di-reply harus berupa foto.")
        return

    await event.edit("🖼️ Memproses gambar...")
    try:
        photo_bytes = await client.download_media(reply.photo, file=bytes)
        img = Image.open(io.BytesIO(photo_bytes)).convert("RGB")

        new_size = (img.width * scale, img.height * scale)
        img = img.resize(new_size, Image.LANCZOS)
        img = img.filter(ImageFilter.SHARPEN)

        color = ImageEnhance.Color(img)
        img = color.enhance(1.2)
        contrast = ImageEnhance.Contrast(img)
        img = contrast.enhance(1.1)

        buf = io.BytesIO()
        buf.name = "upscaled.png"
        img.save(buf, "PNG")
        buf.seek(0)

        await event.delete()
        await client.send_file(event.chat_id, buf, caption=f"🖼️ Upscaled {scale}x (resize + sharpen + color boost)")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
