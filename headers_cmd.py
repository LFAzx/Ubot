import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}headers <url>", "Cek HTTP security headers suatu website", "OSINT")

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy",
]


def _check_headers(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    resp = requests.get(url, timeout=15)
    return resp.headers


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}headers (\S+)$"))
async def headers_handler(event):
    url = event.pattern_match.group(1)
    await event.edit("🔎 Cek security headers...")
    try:
        headers = await asyncio.to_thread(_check_headers, url)
        lines = []
        for h in SECURITY_HEADERS:
            if h in headers:
                value = headers[h][:60]
                lines.append(f"✅ {h}: {value}")
            else:
                lines.append(f"❌ {h}: tidak ada")
        await event.edit(f"🔎 **Security Headers: {url}**\n" + "\n".join(lines))
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
