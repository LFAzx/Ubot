import hashlib
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}ship <user1> <user2>", "Hitung compatibility receh 2 nama", "Fun")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}ship (\S+) (\S+)$"))
async def ship_handler(event):
    a = event.pattern_match.group(1)
    b = event.pattern_match.group(2)

    combined = "".join(sorted([a.lower(), b.lower()]))
    h = hashlib.md5(combined.encode()).hexdigest()
    percent = int(h, 16) % 101

    bar_filled = "█" * (percent // 10)
    bar_empty = "░" * (10 - percent // 10)

    await event.edit(f"💘 **{a} + {b}**\n{bar_filled}{bar_empty} {percent}%")
