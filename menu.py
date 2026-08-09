from telethon import events

from client import client, PREFIX, register, COMMANDS

register(f"{PREFIX}menu", "Lihat semua perintah", "Utility")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}menu$"))
async def menu_handler(event):
    categories = {}
    for c in COMMANDS:
        categories.setdefault(c["category"], []).append(c)

    lines = ["**📜 Rezxploit Userbot — Daftar Perintah**\n"]
    for category, cmds in categories.items():
        lines.append(f"**{category}**")
        for c in cmds:
            lines.append(f"`{c['cmd']}` — {c['desc']}")
        lines.append("")

    await event.edit("\n".join(lines))
