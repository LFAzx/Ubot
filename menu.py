from telethon import events

from client import client, PREFIX, register, COMMANDS

register(f"{PREFIX}menu", "Lihat semua perintah", "Utility")

MAX_CHUNK = 3500


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}menu$"))
async def menu_handler(event):
    try:
        categories = {}
        for c in COMMANDS:
            categories.setdefault(c["category"], []).append(c)

        chunks = []
        current = "**📜 SilentCyber Userbot — Daftar Perintah**\n"

        for category, cmds in categories.items():
            block = f"\n**{category}**\n"
            for c in cmds:
                block += f"`{c['cmd']}` — {c['desc']}\n"

            if len(current) + len(block) > MAX_CHUNK:
                chunks.append(current)
                current = block
            else:
                current += block

        if current:
            chunks.append(current)

        await event.edit(chunks[0])
        for chunk in chunks[1:]:
            await client.send_message(event.chat_id, chunk)
    except Exception as e:
        await event.edit(f"❌ Error nampilin menu: {e}")
