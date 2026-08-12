from telethon import events
import io
import qrcode

from client import client, PREFIX, register

register(f"{PREFIX}qrbatch <teks1>|<teks2>|...", "Generate banyak QR sekaligus (pisah pakai |)", "Utility")

MAX_BATCH = 10


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}qrbatch (.+)$"))
async def qrbatch_handler(event):
    items = [i.strip() for i in event.pattern_match.group(1).split("|") if i.strip()]
    items = items[:MAX_BATCH]

    if not items:
        await event.edit("⚠️ Kasih minimal 1 teks, pisah pakai `|` buat lebih dari 1.")
        return

    await event.edit(f"🔳 Generate {len(items)} QR code...")
    try:
        files = []
        for text in items:
            img = qrcode.make(text)
            buf = io.BytesIO()
            buf.name = "qr.png"
            img.save(buf, "PNG")
            buf.seek(0)
            files.append(buf)

        await event.delete()
        await client.send_file(event.chat_id, files, caption="🔳 " + " | ".join(items))
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
