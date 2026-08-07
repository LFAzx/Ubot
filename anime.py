import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}anime <judul>", "Cari info anime (AniList)", "Utility")

QUERY = """
query ($search: String) {
  Media(search: $search, type: ANIME) {
    title { romaji english }
    averageScore
    status
    episodes
    description(asHtml: false)
  }
}
"""


def _search_anime(title):
    resp = requests.post(
        "https://graphql.anilist.co",
        json={"query": QUERY, "variables": {"search": title}},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    media = data.get("data", {}).get("Media")
    if not media:
        raise Exception("Anime gak ditemukan.")
    return media


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}anime (.+)$"))
async def anime_handler(event):
    title = event.pattern_match.group(1)
    await event.edit("🔎 Cari anime...")
    try:
        a = await asyncio.to_thread(_search_anime, title)
        name = a["title"].get("english") or a["title"].get("romaji")
        score = a.get("averageScore", "?")
        status = a.get("status", "?")
        episodes = a.get("episodes", "?")
        desc = (a.get("description") or "-").replace("<br>", "\n")[:400]

        text = (
            f"**🎬 {name}**\n"
            f"Score: {score}\n"
            f"Status: {status}\n"
            f"Episodes: {episodes}\n\n"
            f"{desc}..."
        )
        await event.edit(text)
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
