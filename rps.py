import random
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}rps <batu|gunting|kertas>", "Main suit lawan bot", "Fun")

CHOICES = ["batu", "gunting", "kertas"]
BEATS = {"batu": "gunting", "gunting": "kertas", "kertas": "batu"}
EMOJI = {"batu": "🪨", "gunting": "✂️", "kertas": "📄"}


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}rps (batu|gunting|kertas)$"))
async def rps_handler(event):
    player = event.pattern_match.group(1)
    bot_choice = random.choice(CHOICES)

    if player == bot_choice:
        result = "🤝 Seri!"
    elif BEATS[player] == bot_choice:
        result = "🎉 Kamu menang!"
    else:
        result = "😭 Bot menang!"

    await event.edit(f"{EMOJI[player]} vs {EMOJI[bot_choice]}\n{result}")
