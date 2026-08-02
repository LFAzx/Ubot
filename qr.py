import io
from telethon import events
import qrcode

from client import client, PREFIX, register

register(f"{PREFIX}qr <teks>", "Generate QR code", "Utility")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}qr (.+)$"))
async def qr_handler(event):
    text = event.pattern_match.group(1)
    await event.edit("🔳 Generate QR...")
    try:
        img = qrcode.make(text)
        buf = io.BytesIO()
        buf.name = "qr.png"
        img.save(buf, "PNG")
        buf.seek(0)

        await event.delete()
        await client.send_file(event.chat_id, buf, caption=f"🔳 QR: {text}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
