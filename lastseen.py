from telethon import events
from telethon.tl.types import (
    UserStatusOnline, UserStatusOffline, UserStatusRecently,
    UserStatusLastWeek, UserStatusLastMonth,
)

from client import client, PREFIX, register

register(f"{PREFIX}lastseen", "Cek status online terakhir (reply user)", "Utility")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}lastseen$"))
async def lastseen_handler(event):
    if not event.is_reply:
        await event.edit("⚠️ Reply ke pesan dari user yang mau dicek.")
        return

    reply = await event.get_reply_message()
    user = await reply.get_sender()
    status = user.status

    if isinstance(status, UserStatusOnline):
        text = "🟢 Online sekarang"
    elif isinstance(status, UserStatusOffline):
        text = f"⚪ Terakhir online: {status.was_online.strftime('%Y-%m-%d %H:%M UTC')}"
    elif isinstance(status, UserStatusRecently):
        text = "🕐 Baru-baru ini (detail disembunyikan privasi user)"
    elif isinstance(status, UserStatusLastWeek):
        text = "📅 Minggu lalu (detail disembunyikan privasi user)"
    elif isinstance(status, UserStatusLastMonth):
        text = "📆 Bulan lalu (detail disembunyikan privasi user)"
    else:
        text = "❓ Gak bisa dideteksi (privasi disembunyikan total)"

    await event.edit(f"👀 **Last seen {user.first_name}:**\n{text}")
