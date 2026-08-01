import logging
from telethon import events

from client import client, PREFIX, register
from ai import ask_ai

log = logging.getLogger("userbot")

register(f"{PREFIX}ai <prompt>", "Tanya AI (reply pesan juga bisa)", "AI")
register(f"{PREFIX}summarize", "Ringkas pesan yang di-reply", "AI")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}ai(?:\s([\s\S]*))?$"))
async def ai_handler(event):
    prompt = event.pattern_match.group(1)
    prompt = prompt.strip() if prompt else ""

    if not prompt and event.is_reply:
        reply = await event.get_reply_message()
        prompt = reply.raw_text or ""

    if not prompt:
        await event.edit(f"⚠️ Usage: `{PREFIX}ai <pertanyaan>` atau reply pesan.")
        return

    await event.edit("🤔 Mikir...")
    try:
        response = await ask_ai(prompt)
        await event.edit(f"🤖 {response}")
    except Exception as e:
        log.exception("AI command failed")
        await event.edit(f"❌ Error: {e}")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}summarize$"))
async def summarize_handler(event):
    if not event.is_reply:
        await event.edit("⚠️ Reply ke pesan yang mau diringkas.")
        return

    reply = await event.get_reply_message()
    text = reply.raw_text or ""
    if not text.strip():
        await event.edit("⚠️ Pesan yang di-reply gak ada teksnya.")
        return

    await event.edit("📝 Meringkas...")
    try:
        summary = await ask_ai(f"Ringkas teks berikut dalam bahasa Indonesia, singkat dan padat:\n\n{text}")
        await event.edit(f"📝 **Ringkasan:**\n\n{summary}")
    except Exception as e:
        log.exception("Summarize command failed")
        await event.edit(f"❌ Error: {e}")
