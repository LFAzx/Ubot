import json
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}jsonformat", "Rapiin format JSON (reply/ketik langsung)", "Utility")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}jsonformat(?:\s([\s\S]+))?$"))
async def jsonformat_handler(event):
    text = event.pattern_match.group(1)

    if not text and event.is_reply:
        reply = await event.get_reply_message()
        text = reply.raw_text or ""

    if not text:
        await event.edit("⚠️ Kasih JSON-nya atau reply pesan yang isinya JSON.")
        return

    try:
        parsed = json.loads(text)
        formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
        await event.edit(f"```json\n{formatted}\n```")
    except Exception as e:
        await event.edit(f"❌ JSON gak valid: {e}")
