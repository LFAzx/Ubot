from telethon import events
from deep_translator import GoogleTranslator

from client import client, PREFIX, register

register(f"{PREFIX}tr <kode_bahasa> <teks>", "Translate teks (reply juga bisa)", "Utility")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}tr (\w{{2}})(?:\s([\s\S]*))?$"))
async def tr_handler(event):
    lang = event.pattern_match.group(1)
    text = event.pattern_match.group(2)

    if not text and event.is_reply:
        reply = await event.get_reply_message()
        text = reply.raw_text or ""

    if not text:
        await event.edit(f"⚠️ Usage: `{PREFIX}tr <kode_bahasa> <teks>` atau reply pesan. Contoh: `{PREFIX}tr en halo semua`")
        return

    await event.edit("🌐 Menerjemahkan...")
    try:
        result = GoogleTranslator(source="auto", target=lang).translate(text)
        await event.edit(f"🌐 **[{lang}]** {result}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
