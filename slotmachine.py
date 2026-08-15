import random
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}slotmachine", "Main slot machine", "Fun")

SYMBOLS = ["🍒", "🍋", "🍊", "🍇", "💎", "7️⃣"]


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}slotmachine$"))
async def slotmachine_handler(event):
    result = [random.choice(SYMBOLS) for _ in range(3)]
    display = " | ".join(result)

    if result[0] == result[1] == result[2]:
        outcome = "🎉 JACKPOT! Menang besar!"
    elif result[0] == result[1] or result[1] == result[2]:
        outcome = "✨ Lumayan, 2 simbol sama!"
    else:
        outcome = "😅 Coba lagi!"

    await event.edit(f"🎰 {display} 🎰\n{outcome}")
