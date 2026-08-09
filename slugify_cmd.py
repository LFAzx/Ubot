import re
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}slugify <teks>", "Ubah teks jadi format URL-friendly", "Utility")


def _slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}slugify (.+)$"))
async def slugify_handler(event):
    text = event.pattern_match.group(1)
    result = _slugify(text)
    await event.edit(f"🔗 `{result}`")
