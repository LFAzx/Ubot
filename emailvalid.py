import re
import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}emailvalid <email>", "Cek format email + validitas MX record domain", "OSINT")

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _validate_email(email):
    if not EMAIL_RE.match(email):
        return {"format_valid": False, "mx_valid": False}

    domain = email.split("@")[1]
    try:
        resp = requests.get(
            "https://cloudflare-dns.com/dns-query",
            params={"name": domain, "type": "MX"},
            headers={"Accept": "application/dns-json"},
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        answers = data.get("Answer", [])
        mx_valid = len(answers) > 0
    except Exception:
        mx_valid = False

    return {"format_valid": True, "mx_valid": mx_valid}


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}emailvalid (\S+)$"))
async def emailvalid_handler(event):
    email = event.pattern_match.group(1)
    await event.edit("📧 Validasi email...")
    try:
        result = await asyncio.to_thread(_validate_email, email)
        format_mark = "✅" if result["format_valid"] else "❌"
        mx_mark = "✅" if result["mx_valid"] else "❌"

        text = (
            f"📧 **{email}**\n"
            f"Format valid: {format_mark}\n"
            f"Domain punya mail server: {mx_mark}"
        )
        await event.edit(text)
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
