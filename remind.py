import asyncio
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}remind <menit> <pesan>", "Reminder (hilang kalau bot restart)", "Produktivitas")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}remind (\d+) (.+)$"))
async def remind_handler(event):
    minutes = int(event.pattern_match.group(1))
    message = event.pattern_match.group(2)
    chat_id = event.chat_id

    await event.edit(f"⏰ Oke, aku ingetin **{message}** dalam {minutes} menit.")

    async def _remind():
        await asyncio.sleep(minutes * 60)
        await client.send_message(chat_id, f"⏰ **Reminder:** {message}")

    asyncio.create_task(_remind())
