import asyncio
import random
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}mining <coin> <menit>", "Mining crypto gimmick (fake, hiburan doang)", "Fun")

FAKE_STEPS = [
    "Connecting to mining pool...",
    "Authenticating worker...",
    "Fetching job from pool...",
    "Initializing hash engine...",
    "Mining in progress...",
    "Submitting shares...",
    "Verifying share validity...",
]

FAKE_ERRORS = [
    "❌ Error: Mining pool connection lost",
    "❌ Error: Stratum protocol handshake failed",
    "❌ Error: Share rejected — stale job",
    "❌ Error: Worker authentication timeout",
    "❌ Error: Pool server unreachable (timeout)",
    "❌ Error: Hash rate dropped to 0, hardware fault detected",
]


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}mining (\S+) (\d+)$"))
async def mining_handler(event):
    coin = event.pattern_match.group(1).upper()
    minutes = min(int(event.pattern_match.group(2)), 3)

    total_duration = minutes * 60
    step_count = len(FAKE_STEPS)
    step_duration = total_duration / step_count

    for i, step in enumerate(FAKE_STEPS):
        progress = int((i + 1) / step_count * 100)
        bar = ("█" * (progress // 10)).ljust(10, "░")
        fake_hashrate = random.randint(50, 500)
        await event.edit(
            f"⛏️ **Mining {coin}...**\n\n"
            f"[{bar}] {progress}%\n"
            f"Hashrate: {fake_hashrate} H/s\n"
            f"{step}"
        )
        await asyncio.sleep(step_duration)

    error = random.choice(FAKE_ERRORS)
    await event.edit(f"⛏️ **Mining Stopped**\n{error}")
