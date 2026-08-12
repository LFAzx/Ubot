import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}leakcheck <username>", "Cek username pernah bocor di breach mana (Powered by LeakCheck)", "OSINT")


def _check_leak(username):
    resp = requests.get("https://leakcheck.io/api/public", params={"check": username}, timeout=15)
    resp.raise_for_status()
    return resp.json()


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}leakcheck (\S+)$"))
async def leakcheck_handler(event):
    username = event.pattern_match.group(1)
    await event.edit("🔍 Cek breach...")
    try:
        data = await asyncio.to_thread(_check_leak, username)
        sources = data.get("sources") or data.get("result") or []

        if not sources:
            await event.edit(f"✅ **{username}** gak ketemu di breach yang tercatat.")
            return

        lines = []
        for s in sources[:15]:
            name = s.get("name") if isinstance(s, dict) else s
            lines.append(f"- {name}")

        await event.edit(f"⚠️ **{username}** ketemu di breach:\n" + "\n".join(lines) + "\n\n_Powered by LeakCheck_")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
