import time
from telethon import events

from client import client, PREFIX, register, START_TIME

register(f"{PREFIX}uptime", "Lihat berapa lama bot udah nyala", "Utility")


def _format_duration(seconds):
    seconds = int(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    parts = []
    if days:
        parts.append(f"{days}h")
    if hours:
        parts.append(f"{hours}j")
    if minutes:
        parts.append(f"{minutes}m")
    parts.append(f"{seconds}d")
    return " ".join(parts)


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}uptime$"))
async def uptime_handler(event):
    elapsed = time.time() - START_TIME
    await event.edit(f"⏱️ Uptime: {_format_duration(elapsed)}")
