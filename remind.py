import asyncio
import time
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}remind <menit> <pesan>", "Reminder (hilang kalau bot restart)", "Produktivitas")
register(f"{PREFIX}remindlist", "Lihat reminder aktif di chat ini", "Produktivitas")

_active_reminders = {}


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}remind (\d+) (.+)$"))
async def remind_handler(event):
    minutes = int(event.pattern_match.group(1))
    message = event.pattern_match.group(2)
    chat_id = event.chat_id
    fire_at = time.time() + minutes * 60

    await event.edit(f"⏰ Oke, aku ingetin **{message}** dalam {minutes} menit.")

    entry = {"message": message, "fire_at": fire_at}
    _active_reminders.setdefault(chat_id, []).append(entry)

    async def _remind():
        await asyncio.sleep(minutes * 60)
        await client.send_message(chat_id, f"⏰ **Reminder:** {message}")
        if entry in _active_reminders.get(chat_id, []):
            _active_reminders[chat_id].remove(entry)

    asyncio.create_task(_remind())


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}remindlist$"))
async def remindlist_handler(event):
    chat_id = event.chat_id
    reminders = _active_reminders.get(chat_id, [])
    if not reminders:
        await event.edit("📭 Gak ada reminder aktif di chat ini.")
        return

    now = time.time()
    lines = []
    for r in reminders:
        remaining = int(r["fire_at"] - now)
        minutes, seconds = divmod(max(remaining, 0), 60)
        lines.append(f"- {r['message']} (dalam {minutes}m {seconds}d)")

    await event.edit("⏰ **Reminder aktif:**\n" + "\n".join(lines))
