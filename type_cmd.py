import asyncio
from telethon import events

from client import client, PREFIX, register

MAX_LEN = 200
CHUNK = 3

register(f"{PREFIX}type <teks>", f"Efek animasi ngetik (maks {MAX_LEN} karakter)", "Fun")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}type (.+)$"))
async def type_handler(event):
    text = event.pattern_match.group(1)[:MAX_LEN]

    for i in range(0, len(text), CHUNK):
        partial = text[:i + CHUNK]
        await event.edit(partial + "▌")
        await asyncio.sleep(0.15)

    await event.edit(text)
