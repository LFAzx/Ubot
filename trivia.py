import asyncio
import html
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}trivia", "Random pertanyaan trivia", "Fun")


def _get_trivia():
    resp = requests.get("https://opentdb.com/api.php?amount=1", timeout=15)
    resp.raise_for_status()
    data = resp.json()
    result = data.get("results", [])
    if not result:
        raise Exception("Gagal ambil trivia.")
    q = result[0]
    question = html.unescape(q["question"])
    answer = html.unescape(q["correct_answer"])
    return question, answer


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}trivia$"))
async def trivia_handler(event):
    await event.edit("🧠 Cari trivia...")
    try:
        question, answer = await asyncio.to_thread(_get_trivia)
        await event.edit(f"🧠 **Trivia:**\n{question}\n\n**Jawaban:** {answer}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
