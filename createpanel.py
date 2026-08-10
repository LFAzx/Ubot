import asyncio
import random
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}createpanel <username> <password> <domain>", "Panel Pterodactyl creation gimmick (fake, hiburan doang)", "Fun")

FAKE_STEPS = [
    "Cloning Pterodactyl panel repository...",
    "Installing Composer dependencies...",
    "Configuring environment (.env)...",
    "Running database migrations...",
    "Generating application key...",
    "Setting up queue worker...",
    "Configuring Nginx virtual host...",
    "Requesting SSL certificate...",
    "Creating admin account...",
]

FAKE_ERRORS = [
    "❌ Error 403: Forbidden — panel provisioning API menolak request.",
    "❌ Error: Composer dependency resolution failed (package conflict).",
    "❌ Error 500: Database migration gagal, koneksi MySQL timeout.",
    "❌ Error: SSL certificate request ditolak (rate limit Let's Encrypt).",
    "❌ Error 502: Bad Gateway dari provisioning node.",
    "❌ Error: Queue worker gagal start, service crash-loop.",
]


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}createpanel (\S+) (\S+) (\S+)$"))
async def createpanel_handler(event):
    username = event.pattern_match.group(1)
    password = event.pattern_match.group(2)
    domain = event.pattern_match.group(3)

    total_duration = random.randint(60, 180)
    step_count = len(FAKE_STEPS)
    step_duration = total_duration / step_count

    for i, step in enumerate(FAKE_STEPS):
        progress = int((i + 1) / step_count * 100)
        bar = ("█" * (progress // 10)).ljust(10, "░")
        await event.edit(
            f"⚙️ **Creating Pterodactyl Panel...**\n"
            f"Admin: {username} | Domain: {domain}\n\n"
            f"[{bar}] {progress}%\n"
            f"{step}"
        )
        await asyncio.sleep(step_duration)

    error = random.choice(FAKE_ERRORS)
    await event.edit(f"⚙️ **Panel Creation Failed**\n{error}")
