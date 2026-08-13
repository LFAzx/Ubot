import re
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}hashid <hash>", "Deteksi jenis hash dari panjang & pattern", "OSINT")

HASH_PATTERNS = [
    (32, r"^[a-f0-9]{32}$", "MD5"),
    (32, r"^[a-f0-9]{32}$", "NTLM"),
    (40, r"^[a-f0-9]{40}$", "SHA1"),
    (56, r"^[a-f0-9]{56}$", "SHA224"),
    (64, r"^[a-f0-9]{64}$", "SHA256"),
    (96, r"^[a-f0-9]{96}$", "SHA384"),
    (128, r"^[a-f0-9]{128}$", "SHA512"),
]


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}hashid (\S+)$"))
async def hashid_handler(event):
    h = event.pattern_match.group(1).lower()

    matches = []
    for length, pattern, name in HASH_PATTERNS:
        if len(h) == length and re.match(pattern, h):
            matches.append(name)

    if not matches:
        await event.edit(f"❓ Gak dikenali sebagai hash umum (panjang: {len(h)} karakter).")
        return

    await event.edit("🔑 **Kemungkinan jenis hash:**\n" + "\n".join(f"- {m}" for m in matches))
