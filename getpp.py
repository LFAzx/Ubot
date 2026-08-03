import io
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}getpp", "Download foto profil (reply user)", "Media")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}getpp$"))
async def getpp_handler(event):
    if not event.is_reply:
        await event.edit("⚠️ Reply ke pesan dari user yang mau diambil foto profilnya.")
        return

    reply = await event.get_reply_message()
    user = await reply.get_sender()

    await event.edit("🖼️ Download foto profil...")
    try:
        photo_bytes = await client.download_profile_photo(user, file=bytes)
        if not photo_bytes:
            await event.edit("❌ User ini gak punya foto profil.")
            return

        buf = io.BytesIO(photo_bytes)
        buf.name = "avatar.jpg"

        await event.delete()
        await client.send_file(event.chat_id, buf, caption=f"🖼️ Foto profil {user.first_name}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
