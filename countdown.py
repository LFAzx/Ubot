from datetime import datetime
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}countdown <YYYY-MM-DD>", "Hitung mundur ke tanggal tertentu", "Produktivitas")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}countdown (\d{{4}}-\d{{2}}-\d{{2}})$"))
async def countdown_handler(event):
    date_str = event.pattern_match.group(1)
    try:
        target = datetime.strptime(date_str, "%Y-%m-%d")
        now = datetime.now()
        delta = target - now

        if delta.total_seconds() < 0:
            await event.edit(f"📅 Tanggal itu udah lewat {abs(delta.days)} hari yang lalu.")
            return

        await event.edit(f"📅 **{date_str}**\n{delta.days} hari lagi!")
    except Exception as e:
        await event.edit(f"❌ Error: {e} (format: YYYY-MM-DD)")
