import uuid
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}uuid", "Generate UUID random", "Utility")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}uuid$"))
async def uuid_handler(event):
    result = str(uuid.uuid4())
    await event.edit(f"🆔 `{result}`")
