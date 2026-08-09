import asyncio
import random
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}createvps <username> <password> <domain> <ram-ssd>", "Fun")

FAKE_STEPS = [
    "Allocating resources...",
    "Provisioning virtual disk...",
    "Configuring network interface...",
    "Installing base OS image...",
    "Setting up SSH daemon...",
    "Applying firewall rules...",
    "Registering DNS entry...",
    "Finalizing VPS instance...",
]

FAKE_ERRORS = [
    "❌ Error 403: Forbidden — quota provisioning ditolak oleh node cluster.",
    "❌ Error 404: Service has not available now.",
    "❌ Error 502: Bad Gateway dari hypervisor node.",
    "❌ Error 500: Internal provisioning error, resource allocation gagal.",
    "❌ Error 429: Too many requests ke provisioning API, coba lagi nanti.",
    "❌ Error 503: Node cluster sedang maintenance.",
]


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}createvps (\S+) (\S+) (\S+) (\S+)$"))
async def createvps_handler(event):
    username = event.pattern_match.group(1)
    password = event.pattern_match.group(2)
    domain = event.pattern_match.group(3)
    spec = event.pattern_match.group(4)

    total_duration = random.randint(60, 180)
    step_count = len(FAKE_STEPS)
    step_duration = total_duration / step_count

    for i, step in enumerate(FAKE_STEPS):
        progress = int((i + 1) / step_count * 100)
        bar = ("█" * (progress // 10)).ljust(10, "░")
        await event.edit(
            f"🖥️ **Creating VPS...**\n"
            f"User: {username} | Domain: {domain} | Spec: {spec}\n\n"
            f"[{bar}] {progress}%\n"
            f"{step}"
        )
        await asyncio.sleep(step_duration)

    error = random.choice(FAKE_ERRORS)
    await event.edit(f"🖥️ **VPS Creation Failed**\n{error}")
