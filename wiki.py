import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}wiki <topik>", "Ringkasan dari Wikipedia", "Utility")


def _fetch_wiki(topic):
    resp = requests.get(
        f"https://id.wikipedia.org/api/rest_v1/page/summary/{topic}",
        timeout=10,
        headers={"User-Agent": "SilentCyberUserbot/1.0"},
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("extract", "Gak ada ringkasan.")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}wiki (.+)$"))
async def wiki_handler(event):
    topic = event.pattern_match.group(1)
    await event.edit("📖 Cari di Wikipedia...")
    try:
        summary = await asyncio.to_thread(_fetch_wiki, topic.replace(" ", "_"))
        await event.edit(f"📖 **{topic}**\n\n{summary}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
