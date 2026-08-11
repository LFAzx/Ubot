import emoji as emoji_lib
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}emoji <kata>", "Cari emoji berdasarkan kata kunci (bahasa Inggris)", "Fun")


def _search_emoji(keyword):
    keyword = keyword.lower().replace(" ", "_")
    matches = []
    for char, data in emoji_lib.EMOJI_DATA.items():
        name = data.get("en", "")
        if keyword in name.lower():
            matches.append(char)
        if len(matches) >= 15:
            break
    return matches


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}emoji (.+)$"))
async def emoji_handler(event):
    keyword = event.pattern_match.group(1)
    results = _search_emoji(keyword)
    if not results:
        await event.edit(f"❌ Gak nemu emoji buat '{keyword}' (coba kata bahasa Inggris).")
        return
    await event.edit(f"😀 **{keyword}:** " + " ".join(results))
