import re
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}regextest <pattern> <teks>", "Test regex, lihat semua match", "Utility")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}regextest (\S+) (.+)$"))
async def regextest_handler(event):
    pattern = event.pattern_match.group(1)
    text = event.pattern_match.group(2)

    try:
        matches = re.findall(pattern, text)
        if not matches:
            await event.edit(f"❌ Gak ada match buat pattern `{pattern}`.")
            return

        lines = "\n".join(f"- {m}" for m in matches[:20])
        await event.edit(f"✅ **{len(matches)} match ditemukan:**\n{lines}")
    except Exception as e:
        await event.edit(f"❌ Regex error: {e}")
