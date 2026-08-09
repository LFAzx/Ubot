import re
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}wordcount", "Hitung kata/karakter/kalimat (reply pesan)", "Utility")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}wordcount$"))
async def wordcount_handler(event):
    if not event.is_reply:
        await event.edit("⚠️ Reply ke pesan yang mau dihitung.")
        return

    reply = await event.get_reply_message()
    text = reply.raw_text or ""

    if not text.strip():
        await event.edit("⚠️ Pesan yang di-reply gak ada teksnya.")
        return

    words = len(text.split())
    chars = len(text)
    chars_no_space = len(text.replace(" ", ""))
    sentences = len(re.findall(r"[.!?]+", text)) or 1

    await event.edit(
        f"📊 **Word Count**\n"
        f"Kata: {words}\n"
        f"Karakter: {chars} ({chars_no_space} tanpa spasi)\n"
        f"Kalimat: ~{sentences}"
    )
