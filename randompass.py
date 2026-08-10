import secrets
import string
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}randompass <panjang>", "Generate password acak yang aman", "Utility")

CHARS = string.ascii_letters + string.digits + "!@#$%^&*"


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}randompass (\d+)$"))
async def randompass_handler(event):
    length = min(int(event.pattern_match.group(1)), 128)
    if length < 4:
        await event.edit("⚠️ Minimal panjang 4 karakter.")
        return

    password = "".join(secrets.choice(CHARS) for _ in range(length))
    await event.edit(f"🔑 **Password ({length} karakter):**\n`{password}`")
