import asyncio
from telethon import events

from client import client, PREFIX, register

MAX_SPAM = 20

register(f"{PREFIX}spam <teks> <jumlah>", f"Kirim teks berulang (maks {MAX_SPAM}x, ada delay)", "Fun")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}spam (.+) (\d+)$"))
async def spam_handler(event):
    text = event.pattern_match.group(1)
    count = int(event.pattern_match.group(2))

    if count > MAX_SPAM:
        await event.edit(f"⚠️ Maks {MAX_SPAM}x sekali jalan (biar akun aman dari flood limit Telegram).")
        return

    if count < 1:
        await event.edit("⚠️ Jumlah harus minimal 1.")
        return

    await event.delete()
    for _ in range(count):
        await client.send_message(event.chat_id, text)
        await asyncio.sleep(1)
