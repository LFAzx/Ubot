import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}chess", "Bikin link ajakan main catur (Lichess, gratis tanpa akun)", "Fun")


def _create_lichess_challenge():
    resp = requests.post("https://lichess.org/api/challenge/open", timeout=15)
    resp.raise_for_status()
    return resp.json()


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}chess$"))
async def chess_handler(event):
    await event.edit("♟️ Bikin link ajakan catur...")
    try:
        data = await asyncio.to_thread(_create_lichess_challenge)
        url_white = data.get("urlWhite") or data.get("url")
        url_black = data.get("urlBlack") or data.get("url")

        text = (
            "♟️ **Ajakan Main Catur (Lichess)**\n\n"
            f"Klik salah satu, temen kamu klik yang lain:\n"
            f"⚪ White: {url_white}\n"
            f"⚫ Black: {url_black}\n\n"
            "Gak perlu akun Lichess buat main."
        )
        await event.edit(text)
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
