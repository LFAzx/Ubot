import sqlite3
from telethon import events

from client import client, PREFIX, register

DB_PATH = "away.db"


def _init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS blacklist (chat_id INTEGER PRIMARY KEY)")
    conn.commit()
    conn.close()


_init_db()

DEFAULT_MESSAGE = "Lagi sibuk, nanti dibales ya! 🙏"


def _get_setting(key, default=None):
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    conn.close()
    return row[0] if row else default


def _set_setting(key, value):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()


def is_away_enabled():
    return _get_setting("enabled", "0") == "1"


def get_away_message():
    return _get_setting("message", DEFAULT_MESSAGE)


def is_blacklisted(chat_id):
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("SELECT 1 FROM blacklist WHERE chat_id = ?", (chat_id,)).fetchone()
    conn.close()
    return row is not None


register(f"{PREFIX}on", "Aktifin away-mode (auto-reply)", "Away")
register(f"{PREFIX}off", "Matiin away-mode", "Away")
register(f"{PREFIX}offcus <teks>", "Set teks custom away-mode", "Away")
register(f"{PREFIX}blacklist add", "Blacklist chat ini dari auto-reply", "Away")
register(f"{PREFIX}blacklist remove", "Hapus chat ini dari blacklist", "Away")
register(f"{PREFIX}blacklist list", "Lihat semua chat yang di-blacklist", "Away")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}on$"))
async def on_handler(event):
    _set_setting("enabled", "1")
    msg = get_away_message()
    await event.edit(f"🌙 Away-mode **aktif**.\nPesan: {msg}")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}off$"))
async def off_handler(event):
    _set_setting("enabled", "0")
    await event.edit("☀️ Away-mode **nonaktif**.")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}offcus (.+)$"))
async def offcus_handler(event):
    text = event.pattern_match.group(1)
    _set_setting("message", text)
    await event.edit(f"📝 Teks away-mode di-update:\n{text}")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}blacklist add$"))
async def blacklist_add_handler(event):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT OR IGNORE INTO blacklist (chat_id) VALUES (?)", (event.chat_id,))
    conn.commit()
    conn.close()
    await event.edit("🚫 Chat ini di-blacklist dari auto-reply.")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}blacklist remove$"))
async def blacklist_remove_handler(event):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM blacklist WHERE chat_id = ?", (event.chat_id,))
    conn.commit()
    conn.close()
    await event.edit("✅ Chat ini dihapus dari blacklist.")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}blacklist list$"))
async def blacklist_list_handler(event):
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT chat_id FROM blacklist").fetchall()
    conn.close()
    if not rows:
        await event.edit("📭 Belum ada chat yang di-blacklist.")
        return
    lines = [f"`{r[0]}`" for r in rows]
    await event.edit("🚫 **Blacklisted chats:**\n" + "\n".join(lines))


@client.on(events.NewMessage(incoming=True))
async def away_autoreply_handler(event):
    if not is_away_enabled():
        return

    if is_blacklisted(event.chat_id):
        return

    if event.is_private:
        should_reply = True
    else:
        should_reply = bool(event.mentioned)

    if not should_reply:
        return

    sender = await event.get_sender()
    if sender is None or getattr(sender, "bot", False):
        return

    await event.reply(get_away_message())
