import random
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}textgen <jumlah_paragraf>", "Generate lorem ipsum (default 1 paragraf)", "Utility")

LOREM_WORDS = (
    "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod "
    "tempor incididunt ut labore et dolore magna aliqua ut enim ad minim "
    "veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea "
    "commodo consequat duis aute irure dolor in reprehenderit voluptate "
    "velit esse cillum dolore eu fugiat nulla pariatur excepteur sint "
    "occaecat cupidatat non proident sunt in culpa qui officia deserunt "
    "mollit anim id est laborum"
).split()


def _generate_lorem(paragraphs=1):
    result = []
    for _ in range(paragraphs):
        length = random.randint(30, 50)
        words = [random.choice(LOREM_WORDS) for _ in range(length)]
        words[0] = words[0].capitalize()
        result.append(" ".join(words) + ".")
    return "\n\n".join(result)


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}textgen(?:\s(\d+))?$"))
async def textgen_handler(event):
    count = event.pattern_match.group(1)
    count = min(int(count), 5) if count else 1
    await event.edit(_generate_lorem(count))
