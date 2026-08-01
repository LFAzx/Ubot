import os
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

PREFIX = os.environ.get("PREFIX", ".")

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

COMMANDS = []


def register(cmd: str, desc: str, category: str = "Umum"):
    COMMANDS.append({"cmd": cmd, "desc": desc, "category": category})
