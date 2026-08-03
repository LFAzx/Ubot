import base64
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}base64 <encode|decode> <teks>", "Encode/decode base64", "Utility")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}base64 (encode|decode) ([\s\S]+)$"))
async def base64_handler(event):
    mode = event.pattern_match.group(1)
    text = event.pattern_match.group(2)
    try:
        if mode == "encode":
            result = base64.b64encode(text.encode()).decode()
        else:
            result = base64.b64decode(text.encode()).decode()
        await event.edit(f"🔐 {result}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
