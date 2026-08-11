import random
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}tebak start", "Mulai game tebak angka (1-100)", "Fun")
register(f"{PREFIX}tebak <angka>", "Tebak angkanya", "Fun")

_games = {}


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}tebak start$"))
async def tebak_start_handler(event):
    chat_id = event.chat_id
    _games[chat_id] = {"number": random.randint(1, 100), "tries": 0}
    await event.edit("🎯 Aku udah pilih angka 1-100. Tebak pake `.tebak <angka>`!")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}tebak (\d+)$"))
async def tebak_guess_handler(event):
    chat_id = event.chat_id
    game = _games.get(chat_id)
    if not game:
        await event.edit(f"⚠️ Belum ada game aktif. Mulai dengan `{PREFIX}tebak start`.")
        return

    guess = int(event.pattern_match.group(1))
    game["tries"] += 1

    if guess == game["number"]:
        tries = game["tries"]
        del _games[chat_id]
        await event.edit(f"🎉 Bener! Angkanya {guess}. Ketebak dalam {tries}x coba.")
    elif guess < game["number"]:
        await event.edit("📈 Lebih besar lagi!")
    else:
        await event.edit("📉 Lebih kecil lagi!")
