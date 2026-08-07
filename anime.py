import asyncio
import time
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}anime <judul>", "Cari info anime (MyAnimeList)", "Utility")


def _search_anime(title, retries=3):
    last_error = None
    for attempt in range(retries):
        try:
            resp = requests.get(
                "https://api.jikan.moe/v4/anime",
                params={"q": title, "limit": 1},
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json().get("data", [])
            if not data:
                raise Exception("Anime gak ditemukan.")
            return data[0]
        except requests.exceptions.HTTPError as e:
            last_error = e
            if resp.status_code in (502, 503, 504):
                time.sleep(2)
                continue
            raise
        except requests.exceptions.RequestException as e:
            last_error = e
            time.sleep(2)
    raise Exception(f"Server Jikan lagi bermasalah, coba lagi nanti. ({last_error})")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}anime (.+)$"))
async def anime_handler(event):
    title = event.pattern_match.group(1)
    await event.edit("🔎 Cari anime...")
    try:
        a = await asyncio.to_thread(_search_anime, title)
        name = a.get("title")
        score = a.get("score", "?")
        status = a.get("status", "?")
        episodes = a.get("episodes", "?")
        synopsis = (a.get("synopsis") or "-")[:400]

        text = (
            f"**🎬 {name}**\n"
            f"Score: {score}\n"
            f"Status: {status}\n"
            f"Episodes: {episodes}\n\n"
            f"{synopsis}..."
        )
        await event.edit(text)
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
