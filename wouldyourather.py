import random
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}wouldyourather", "Random pertanyaan would-you-rather", "Fun")

QUESTIONS = [
    ("punya kemampuan terbang", "punya kemampuan baca pikiran orang"),
    ("kaya raya tapi kesepian", "pas-pasan tapi dikelilingi orang yang sayang"),
    ("hidup tanpa internet seumur hidup", "hidup tanpa AC/kipas angin seumur hidup"),
    ("selalu telat 10 menit", "selalu kepagian 10 menit"),
    ("bisa ngomong sama hewan", "bisa ngomong semua bahasa manusia"),
    ("kerja remote selamanya", "kerja kantoran tapi gaji 2x lipat"),
    ("gak bisa makan pedas lagi", "gak bisa minum manis lagi"),
    ("terkenal tapi dibenci", "gak terkenal tapi disayang semua orang deket kamu"),
]


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}wouldyourather$"))
async def wouldyourather_handler(event):
    a, b = random.choice(QUESTIONS)
    await event.edit(f"🤔 **Would you rather...**\nA: {a}\n\natau\n\nB: {b}")
