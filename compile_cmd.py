import asyncio
import random
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}compile <file>", "Compile project gimmick (fake, hiburan doang)", "Fun")

FAKE_STEPS = [
    "Resolving dependencies...",
    "Fetching packages from registry...",
    "Compiling source files...",
    "Linking object files...",
    "Optimizing build (release mode)...",
    "Running static analysis...",
    "Bundling assets...",
    "Finalizing build output...",
]

FAKE_ERRORS = [
    "❌ Error: Segmentation fault (core dumped)",
    "❌ Build failed: undefined reference to symbol at link stage",
    "❌ Error: out of memory during compilation",
    "❌ Fatal error: circular dependency detected",
    "❌ Build failed: incompatible toolchain version",
    "❌ Error: disk quota exceeded during build",
]


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}compile (\S+)$"))
async def compile_handler(event):
    filename = event.pattern_match.group(1)

    total_duration = random.randint(60, 180)
    step_count = len(FAKE_STEPS)
    step_duration = total_duration / step_count

    for i, step in enumerate(FAKE_STEPS):
        progress = int((i + 1) / step_count * 100)
        bar = ("█" * (progress // 10)).ljust(10, "░")
        await event.edit(
            f"🛠️ **Compiling {filename}...**\n\n"
            f"[{bar}] {progress}%\n"
            f"{step}"
        )
        await asyncio.sleep(step_duration)

    error = random.choice(FAKE_ERRORS)
    await event.edit(f"🛠️ **Build Failed**\n{error}")
