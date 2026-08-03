from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}caesar <teks> <geser>", "Caesar cipher (geser negatif buat decode)", "Fun")


def _caesar_shift(text, shift):
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return "".join(result)


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}caesar (.+) (-?\d+)$"))
async def caesar_handler(event):
    text = event.pattern_match.group(1)
    shift = int(event.pattern_match.group(2))
    result = _caesar_shift(text, shift)
    await event.edit(f"🔐 {result}")
