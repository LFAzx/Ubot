import random
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}compliment", "Kasih pujian random (reply user)", "Fun")
register(f"{PREFIX}roast", "Kasih roasting receh (reply user)", "Fun")

COMPLIMENTS = [
    "orangnya asik banget diajak ngobrol.",
    "punya selera humor yang bagus.",
    "keliatan smart dari cara ngomongnya.",
    "vibes-nya positif banget, bikin nyaman.",
    "punya potensi buat sukses gede.",
]

ROASTS = [
    "chat-nya lama banget kayak nunggu loading internet 2G.",
    "kalo lomba telat, pasti juara 1.",
    "julukan 'raja php' kayaknya cocok buat kamu.",
    "modal PD doang tapi followers masih tiga digit.",
    "kalo jadi WiFi, sinyalnya putus-putus terus.",
]


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}compliment$"))
async def compliment_handler(event):
    if not event.is_reply:
        await event.edit("⚠️ Reply ke user yang mau dipuji.")
        return
    reply = await event.get_reply_message()
    user = await reply.get_sender()
    line = random.choice(COMPLIMENTS)
    await event.edit(f"✨ {user.first_name} {line}")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}roast$"))
async def roast_handler(event):
    if not event.is_reply:
        await event.edit("⚠️ Reply ke user yang mau di-roasting.")
        return
    reply = await event.get_reply_message()
    user = await reply.get_sender()
    line = random.choice(ROASTS)
    await event.edit(f"🔥 {user.first_name} {line}")
