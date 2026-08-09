import hashlib
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}rate <teks>", "Kasih rating receh 1-100 buat apapun", "Fun")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}rate (.+)$"))
async def rate_handler(event):
    text = event.pattern_match.group(1)
    h = hashlib.md5(text.lower().encode()).hexdigest()
    percent = int(h, 16) % 101

    await event.edit(f"⭐ **{text}**\nRating: {percent}/100")
