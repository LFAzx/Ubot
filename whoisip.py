import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}whoisip <ip>", "Cek ASN & organisasi pemilik IP", "OSINT")


def _whois_ip(ip):
    resp = requests.get(
        f"http://ip-api.com/json/{ip}",
        params={"fields": "status,message,query,as,asname,isp,org,hosting,mobile,proxy"},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") != "success":
        raise Exception(data.get("message", "Gagal lookup"))
    return data


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}whoisip (\S+)$"))
async def whoisip_handler(event):
    ip = event.pattern_match.group(1)
    await event.edit("🔎 Lookup ASN/organisasi...")
    try:
        data = await asyncio.to_thread(_whois_ip, ip)
        flags = []
        if data.get("hosting"):
            flags.append("Hosting/Datacenter")
        if data.get("proxy"):
            flags.append("Proxy/VPN terdeteksi")
        if data.get("mobile"):
            flags.append("Mobile network")

        text = (
            f"🔎 **{data.get('query')}**\n"
            f"ASN: {data.get('as')}\n"
            f"AS Name: {data.get('asname')}\n"
            f"ISP: {data.get('isp')}\n"
            f"Org: {data.get('org')}\n"
        )
        if flags:
            text += f"Flags: {', '.join(flags)}"
        await event.edit(text)
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
