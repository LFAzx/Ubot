from telethon import events
from telethon.extensions import markdown as md_ext

from client import client, PREFIX, register

register(f"{PREFIX}markdown", "Lihat raw markdown dari pesan yang di-reply", "Utility")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}markdown$"))
async def markdown_handler(event):
    if not event.is_reply:
        await event.edit("⚠️ Reply ke pesan yang mau dilihat raw markdown-nya.")
        return

    reply = await event.get_reply_message()
    if not reply.message:
        await event.edit("⚠️ Pesan yang di-reply gak ada teksnya.")
        return

    try:
        raw = md_ext.unparse(reply.message, reply.entities or [])
        await event.edit(f"```\n{raw}\n```")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
