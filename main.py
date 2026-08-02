import asyncio
import logging

from client import client

import ai_features
import utility
import translate_cmd
import notes
import sticker
import tts
import remind
import media
import spam
import away
import weather
import shorturl
import qr
import purge
import type_cmd
import wiki
import menu

from telethon import events

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("userbot")


@client.on(events.NewMessage())
async def debug_all_handler(event):
    log.info(f"[DEBUG] out={event.out} text={event.raw_text!r} chat_id={event.chat_id}")


async def main():
    await client.start()
    me = await client.get_me()
    log.info(f"Userbot started as {me.first_name} (@{me.username})")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
