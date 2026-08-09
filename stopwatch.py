import time
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}stopwatch <start|stop>", "Stopwatch manual", "Produktivitas")

_stopwatches = {}


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}stopwatch (start|stop)$"))
async def stopwatch_handler(event):
    action = event.pattern_match.group(1)
    chat_id = event.chat_id

    if action == "start":
        _stopwatches[chat_id] = time.time()
        await event.edit("⏱️ Stopwatch dimulai.")
    else:
        start_time = _stopwatches.pop(chat_id, None)
        if start_time is None:
            await event.edit("⚠️ Stopwatch belum di-start di chat ini.")
            return
        elapsed = time.time() - start_time
        minutes, seconds = divmod(int(elapsed), 60)
        await event.edit(f"⏱️ Stopwatch berhenti: {minutes}m {seconds}d")
