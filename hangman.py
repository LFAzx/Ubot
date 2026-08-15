import random
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}hangman start", "Mulai game hangman (tebak kata)", "Fun")
register(f"{PREFIX}hangman <huruf>", "Tebak 1 huruf", "Fun")

WORDS = [
    "python", "telegram", "cyber", "keyboard", "internet",
    "security", "database", "developer", "railway", "hosting",
]

_games = {}
MAX_WRONG = 6


def _render(word, guessed):
    return " ".join(c if c in guessed else "_" for c in word)


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}hangman start$"))
async def hangman_start_handler(event):
    chat_id = event.chat_id
    word = random.choice(WORDS)
    _games[chat_id] = {"word": word, "guessed": set(), "wrong": 0}

    await event.edit(
        f"🪢 **Hangman dimulai!**\n"
        f"{_render(word, set())}\n"
        f"Salah: 0/{MAX_WRONG}\n\n"
        f"Tebak huruf pake `{PREFIX}hangman <huruf>`"
    )


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}hangman ([a-zA-Z])$"))
async def hangman_guess_handler(event):
    chat_id = event.chat_id
    game = _games.get(chat_id)
    if not game:
        await event.edit(f"⚠️ Belum ada game aktif. Mulai dengan `{PREFIX}hangman start`.")
        return

    letter = event.pattern_match.group(1).lower()
    word = game["word"]

    if letter in game["guessed"]:
        await event.edit("⚠️ Huruf itu udah pernah ditebak.")
        return

    game["guessed"].add(letter)
    if letter not in word:
        game["wrong"] += 1

    display = _render(word, game["guessed"])

    if "_" not in display:
        del _games[chat_id]
        await event.edit(f"🎉 **Menang!** Katanya: {word}")
        return

    if game["wrong"] >= MAX_WRONG:
        del _games[chat_id]
        await event.edit(f"💀 **Kalah!** Katanya: {word}")
        return

    await event.edit(f"🪢 {display}\nSalah: {game['wrong']}/{MAX_WRONG}")
