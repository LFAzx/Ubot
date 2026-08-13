import random
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}fortune", "Random fortune cookie ala peruntungan", "Fun")

FORTUNES = [
    "Rezeki gak akan salah alamat, tapi jangan lupa jemput bola.",
    "Hari ini kesempatan baik buat mulai sesuatu yang tertunda.",
    "Orang yang sabar hari ini bakal panen hasil manis besok.",
    "Jangan takut gagal, takutlah kalau gak pernah coba.",
    "Sesuatu yang kamu tunggu bakal datang lebih cepat dari dugaan.",
    "Hati-hati sama keputusan besar minggu ini, pikir dua kali.",
    "Pertemanan baru bakal bawa peluang gak terduga.",
    "Energi positif kamu hari ini nular ke orang sekitar.",
]


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}fortune$"))
async def fortune_handler(event):
    quote = random.choice(FORTUNES)
    await event.edit(f"🥠 {quote}")
