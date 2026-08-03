from telethon import events

from client import client, PREFIX, register
from away import is_away_enabled, get_away_message

register(f"{PREFIX}status", "Cek status away-mode", "Utility")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}status$"))
async def status_handler(event):
    away_state = "🌙 Aktif" if is_away_enabled() else "☀️ Nonaktif"
    msg = get_away_message()
    await event.edit(f"**📊 Status Bot**\nAway-mode: {away_state}\nPesan away: {msg}")
