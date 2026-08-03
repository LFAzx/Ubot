import hashlib
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}hash <teks>", "Generate MD5 & SHA256 hash", "Utility")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}hash (.+)$"))
async def hash_handler(event):
    text = event.pattern_match.group(1)
    md5 = hashlib.md5(text.encode()).hexdigest()
    sha256 = hashlib.sha256(text.encode()).hexdigest()
    await event.edit(f"🔑 **MD5:** `{md5}`\n**SHA256:** `{sha256}`")
