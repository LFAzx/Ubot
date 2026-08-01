import math
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}ping", "Cek bot hidup", "Utility")
register(f"{PREFIX}id", "Lihat chat ID / user ID", "Utility")
register(f"{PREFIX}calc <ekspresi>", "Kalkulator", "Utility")
register(f"{PREFIX}reverse <teks>", "Balik teks", "Utility")
register(f"{PREFIX}ascii <teks>", "Bikin ASCII banner", "Utility")

SAFE_NAMES = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}ping$"))
async def ping_handler(event):
    await event.edit("🏓 Pong!")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}id$"))
async def id_handler(event):
    sender = await event.get_sender()
    text = f"**Chat ID:** `{event.chat_id}`\n**Your ID:** `{sender.id}`"
    if event.is_reply:
        reply = await event.get_reply_message()
        text += f"\n**Replied Msg ID:** `{reply.id}`\n**Replied User ID:** `{reply.sender_id}`"
    await event.edit(text)


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}calc (.+)$"))
async def calc_handler(event):
    expr = event.pattern_match.group(1)
    try:
        result = eval(expr, {"__builtins__": {}}, SAFE_NAMES)
        await event.edit(f"🧮 `{expr}` = **{result}**")
    except Exception as e:
        await event.edit(f"❌ Ekspresi gak valid: {e}")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}reverse (.+)$"))
async def reverse_handler(event):
    text = event.pattern_match.group(1)
    await event.edit(text[::-1])


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}ascii (.+)$"))
async def ascii_handler(event):
    text = event.pattern_match.group(1)
    try:
        import pyfiglet
        banner = pyfiglet.figlet_format(text)
        await event.edit(f"```\n{banner}\n```")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
