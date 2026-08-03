import asyncio
from telethon import events

from client import client, PREFIX, register

MAX_DURATION = 60

register(f"{PREFIX}typefake <detik>", f"Nunjukin 'sedang mengetik' tanpa kirim pesan (maks {MAX_DURATION} detik)", "Fun")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}typefake (\d+)$"))
async def typefake_handler(event):
    duration = min(int(event.pattern_match.group(1)), MAX_DURATION)
    chat_id = event.chat_id

    await event.delete()
    async with client.action(chat_id, "typing"):
        await asyncio.sleep(duration)
