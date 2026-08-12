from urllib.parse import quote_plus
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}googledork <query> <site>", "Generate link Google Dork search", "OSINT")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}googledork (.+) (\S+)$"))
async def googledork_handler(event):
    query = event.pattern_match.group(1)
    site = event.pattern_match.group(2)

    dork = f"{query} site:{site}"
    url = f"https://www.google.com/search?q={quote_plus(dork)}"

    await event.edit(f"🔍 **Google Dork:**\n`{dork}`\n\n{url}")
