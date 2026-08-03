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
import ssweb
import whois_cmd
import textgen
import hash_cmd
import base64_cmd
import quote_cmd
import status_cmd
import uptime_cmd
import typefake
import currency
import searchpin
import menu

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("userbot")


async def main():
    await client.start()
    me = await client.get_me()
    log.info(f"Userbot started as {me.first_name} (@{me.username})")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
