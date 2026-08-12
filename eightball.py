import random
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}8ball <pertanyaan>", "Magic 8-ball klasik", "Fun")

ANSWERS = [
    "Ya, pasti.", "Kemungkinan besar iya.", "Menurutku iya.",
    "Fokus dan tanya lagi.", "Coba tanya lagi nanti.", "Mendingan gak usah dijawab sekarang.",
    "Jangan berharap.", "Jawabanku enggak.", "Sumber-sumber bilang enggak.",
    "Kelihatannya enggak deh.", "Yakin banget iya.", "Tanda-tandanya mengarah ke iya.",
]


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}8ball (.+)$"))
async def eightball_handler(event):
    question = event.pattern_match.group(1)
    answer = random.choice(ANSWERS)
    await event.edit(f"🎱 **{question}**\n{answer}")
