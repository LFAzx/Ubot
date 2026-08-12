import re
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}minify", "Compress kode - hapus baris kosong & whitespace berlebih (reply kode)", "Utility")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}minify$"))
async def minify_handler(event):
    if not event.is_reply:
        await event.edit("⚠️ Reply ke pesan berisi kode yang mau di-minify.")
        return

    reply = await event.get_reply_message()
    code = reply.raw_text or ""

    if not code.strip():
        await event.edit("⚠️ Pesan yang di-reply gak ada isinya.")
        return

    lines = [line.strip() for line in code.splitlines() if line.strip()]
    minified = "\n".join(lines)
    minified = re.sub(r"[ \t]{2,}", " ", minified)

    await event.edit(f"📦 **Minified:**\n```\n{minified}\n```")
