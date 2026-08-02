from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}purge <jumlah>", "Hapus N pesan terakhir kamu di chat ini", "Utility")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}purge (\d+)$"))
async def purge_handler(event):
    count = int(event.pattern_match.group(1))
    chat_id = event.chat_id

    await event.delete()

    deleted = 0
    async for msg in client.iter_messages(chat_id, from_user="me", limit=count):
        await msg.delete()
        deleted += 1

    await client.send_message(chat_id, f"🧹 {deleted} pesan dihapus.")
