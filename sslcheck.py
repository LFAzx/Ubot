import ssl
import socket
import asyncio
from datetime import datetime
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}sslcheck <domain>", "Cek detail SSL certificate", "OSINT")


def _check_ssl(domain):
    ctx = ssl.create_default_context()
    with socket.create_connection((domain, 443), timeout=10) as sock:
        with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
            cert = ssock.getpeercert()

    issuer = dict(x[0] for x in cert.get("issuer", []))
    subject = dict(x[0] for x in cert.get("subject", []))
    not_after = cert.get("notAfter")
    expiry = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
    days_left = (expiry - datetime.utcnow()).days

    return {
        "issuer": issuer.get("organizationName", issuer.get("commonName", "?")),
        "subject": subject.get("commonName", "?"),
        "expires": expiry.strftime("%Y-%m-%d"),
        "days_left": days_left,
    }


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}sslcheck (\S+)$"))
async def sslcheck_handler(event):
    domain = event.pattern_match.group(1)
    await event.edit("🔒 Cek SSL certificate...")
    try:
        info = await asyncio.to_thread(_check_ssl, domain)
        text = (
            f"🔒 **SSL Certificate: {domain}**\n"
            f"Issuer: {info['issuer']}\n"
            f"Subject: {info['subject']}\n"
            f"Expires: {info['expires']} ({info['days_left']} hari lagi)"
        )
        await event.edit(text)
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
