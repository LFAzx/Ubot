import asyncio
import logging

from client import client
from webserver import start_webserver

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
import getpp
import userinfo
import ocr
import qrread
import ip_cmd
import caesar
import searchyt
import lens
import anime
import crypto_cmd
import lastseen
import expand
import pastebin_cmd
import timezone_cmd
import ship
import rate
import acronym
import holiday
import ping2
import slugify_cmd
import wordcount
import dadjoke
import trivia
import stopwatch
import ytmp3
import createvps
import freeproxy
import upscale
import drive_cmd
import createpanel
import infousertt
import infouseryt
import infonewscyber
import searchnews
import menu

from telethon import events

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("userbot")


@client.on(events.NewMessage())
async def debug_all_handler(event):
    log.info(f"[DEBUG] out={event.out} text={event.raw_text!r} chat_id={event.chat_id}")


async def main():
    await start_webserver()
    await client.start()
    me = await client.get_me()
    log.info(f"Userbot started as {me.first_name} (@{me.username})")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
