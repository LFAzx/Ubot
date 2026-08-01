import os
import asyncio
import logging
from telethon import TelegramClient, events
from telethon.sessions import StringSession

from ai import ask_ai

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("userbot")

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

PREFIX = os.environ.get("PREFIX", ".")

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)


def cmd(name: str):
    """Helper to build a command pattern like .ping"""
    return rf"^\{PREFIX}{name}(?: |$)(.*)"


# ---------- Utility ----------

@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}ping$"))
async def ping_handler(event):
    await event.edit("🏓 Pong!")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}id$"))
async def id_handler(event):
    chat = await event.get_chat()
    sender = await event.get_sender()
    text = f"**Chat ID:** `{event.chat_id}`\n**Your ID:** `{sender.id}`"
    if event.is_reply:
        reply = await event.get_reply_message()
        text += f"\n**Replied Msg ID:** `{reply.id}`\n**Replied User ID:** `{reply.sender_id}`"
    await event.edit(text)


# ---------- AI (Groq) ----------

@client.on(events.NewMessage(outgoing=True, pattern=cmd("ai")))
async def ai_handler(event):
    prompt = event.pattern_match.group(1).strip()

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
        await event.edit(f"⚠️ Reply ke pesan yang mau diringkas.")
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


async def main():
    await client.start()
    me = await client.get_me()
    log.info(f"Userbot started as {me.first_name} (@{me.username})")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())

