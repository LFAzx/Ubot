import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}breachcheck <email>", "Cek apakah email pernah bocor di data breach", "Utility")


def _check_breach(email):
    resp = requests.get(f"https://api.xposedornot.com/v1/check-email/{email}", timeout=15)
    resp.raise_for_status()
    data = resp.json()
    return data.get("breaches", [])


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}breachcheck (\S+)$"))
async def breachcheck_handler(event):
    email = event.pattern_match.group(1)
    await event.edit("🔍 Cek data breach...")
    try:
        breaches = await asyncio.to_thread(_check_breach, email)
        flat = [b for group in breaches for b in group] if breaches and isinstance(breaches[0], list) else breaches

        if not flat:
            await event.edit(f"✅ **{email}** gak ketemu di breach yang tercatat.")
            return

        lines = "\n".join(f"- {b}" for b in flat[:15])
        await event.edit(f"⚠️ **{email}** ketemu di {len(flat)} breach:\n{lines}")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
