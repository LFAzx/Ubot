import io
from telethon import events
from PIL import Image, ImageDraw

from client import client, PREFIX, register

register(f"{PREFIX}colorpalette", "Extract warna dominan dari foto (reply foto)", "Media")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}colorpalette$"))
async def colorpalette_handler(event):
    if not event.is_reply:
        await event.edit("⚠️ Reply ke foto yang mau di-extract warnanya.")
        return

    reply = await event.get_reply_message()
    if not reply.photo:
        await event.edit("⚠️ Pesan yang di-reply harus berupa foto.")
        return

    await event.edit("🎨 Extract warna dominan...")
    try:
        photo_bytes = await client.download_media(reply.photo, file=bytes)
        img = Image.open(io.BytesIO(photo_bytes)).convert("RGB")
        img.thumbnail((150, 150))

        quantized = img.quantize(colors=6, method=Image.MEDIANCUT)
        palette = quantized.getpalette()
        color_counts = sorted(quantized.getcolors(), reverse=True)

        colors = []
        for count, idx in color_counts[:6]:
            r, g, b = palette[idx * 3:idx * 3 + 3]
            colors.append(f"#{r:02X}{g:02X}{b:02X}")

        preview = Image.new("RGB", (300, 60))
        draw = ImageDraw.Draw(preview)
        draw_width = 300 // len(colors)
        for i, hexcolor in enumerate(colors):
            rgb = tuple(int(hexcolor[j:j + 2], 16) for j in (1, 3, 5))
            draw.rectangle([i * draw_width, 0, (i + 1) * draw_width, 60], fill=rgb)

        buf = io.BytesIO()
        buf.name = "palette.png"
        preview.save(buf, "PNG")
        buf.seek(0)

        await event.delete()
        await client.send_file(event.chat_id, buf, caption="🎨 " + " ".join(colors))
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
