import io
from telethon import events
from gtts import gTTS

from client import client, PREFIX, register

register(f"{PREFIX}tts <teks>", "Ubah teks jadi voice note (reply juga bisa)", "Media")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}tts(?:\s([\s\S]*))?$"))
async def tts_handler(event):
    text = event.pattern_match.group(1)
    text = text.strip() if text else ""

    if not text and event.is_reply:
        reply = await event.get_reply_message()
        text = reply.raw_text or ""

    if not text:
        await event.edit(f"⚠️ Usage: `{PREFIX}tts <teks>` atau reply pesan.")
        return

    await event.edit("🔊 Membuat voice note...")
    try:
        buf = io.BytesIO()
        gTTS(text=text, lang="id").write_to_fp(buf)
        buf.seek(0)
        buf.name = "tts.mp3"

        await event.delete()
        await client.send_file(event.chat_id, buf, voice_note=True)
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
