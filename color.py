import io
from telethon import events
from PIL import Image

from client import client, PREFIX, register

register(f"{PREFIX}color <hex>", "Preview warna dari kode hex", "Utility")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}color (#?[0-9a-fA-F]{{6}})$"))
async def color_handler(event):
    hex_code = event.pattern_match.group(1).lstrip("#")
    await event.edit("🎨 Generate preview warna...")
    try:
        rgb = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
        img = Image.new("RGB", (300, 300), rgb)

        buf = io.BytesIO()
        buf.name = "color.png"
        img.save(buf, "PNG")
        buf.seek(0)

        await event.delete()
        await client.send_file(event.chat_id, buf, caption=f"🎨 #{hex_code.upper()} — RGB{rgb}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
