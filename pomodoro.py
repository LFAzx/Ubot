import asyncio
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}pomodoro", "Timer pomodoro (25 menit fokus)", "Produktivitas")

FOCUS_MINUTES = 25
BREAK_MINUTES = 5


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}pomodoro$"))
async def pomodoro_handler(event):
    chat_id = event.chat_id
    await event.edit(f"🍅 Pomodoro dimulai! Fokus {FOCUS_MINUTES} menit...")

    async def _run():
        await asyncio.sleep(FOCUS_MINUTES * 60)
        await client.send_message(chat_id, f"🍅 **{FOCUS_MINUTES} menit fokus selesai!** Istirahat {BREAK_MINUTES} menit dulu yuk.")
        await asyncio.sleep(BREAK_MINUTES * 60)
        await client.send_message(chat_id, "⏰ **Istirahat selesai!** Siap lanjut fokus lagi?")

    asyncio.create_task(_run())
