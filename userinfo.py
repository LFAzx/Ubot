from telethon import events
from telethon.tl.functions.users import GetFullUserRequest

from client import client, PREFIX, register

register(f"{PREFIX}userinfo", "Info detail user (reply user, kosong = diri sendiri)", "Utility")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}userinfo$"))
async def userinfo_handler(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        user = await reply.get_sender()
    else:
        user = await event.get_sender()

    await event.edit("🔍 Ambil info user...")
    try:
        full = await client(GetFullUserRequest(user.id))
        bio = full.full_user.about or "-"

        name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "-"
        username = f"@{user.username}" if user.username else "-"
        premium = "Ya" if getattr(user, "premium", False) else "Tidak"

        text = (
            f"**👤 User Info**\n"
            f"Nama: {name}\n"
            f"Username: {username}\n"
            f"ID: `{user.id}`\n"
            f"Premium: {premium}\n"
            f"Bio: {bio}\n"
            f"Chat ID: `{event.chat_id}`"
        )
        await event.edit(text)
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
