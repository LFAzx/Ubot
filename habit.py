import sqlite3
from datetime import date
from telethon import events

from client import client, PREFIX, register

DB_PATH = "habits.db"


def _init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS habits (
        chat_id INTEGER,
        name TEXT,
        PRIMARY KEY (chat_id, name)
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS habit_checks (
        chat_id INTEGER,
        name TEXT,
        check_date TEXT,
        PRIMARY KEY (chat_id, name, check_date)
    )""")
    conn.commit()
    conn.close()


_init_db()

register(f"{PREFIX}habit add <nama>", "Tambah habit baru buat di-track", "Produktivitas")
register(f"{PREFIX}habit check <nama>", "Tandai habit selesai hari ini", "Produktivitas")
register(f"{PREFIX}habit list", "Lihat semua habit + jumlah check-in", "Produktivitas")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}habit add (.+)$"))
async def habit_add_handler(event):
    name = event.pattern_match.group(1)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT OR IGNORE INTO habits (chat_id, name) VALUES (?, ?)", (event.chat_id, name))
    conn.commit()
    conn.close()
    await event.edit(f"✅ Habit baru: **{name}**")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}habit check (.+)$"))
async def habit_check_handler(event):
    name = event.pattern_match.group(1)
    today = date.today().isoformat()

    conn = sqlite3.connect(DB_PATH)
    exists = conn.execute("SELECT 1 FROM habits WHERE chat_id = ? AND name = ?", (event.chat_id, name)).fetchone()
    if not exists:
        conn.close()
        await event.edit(f"⚠️ Habit **{name}** belum ada, tambah dulu pake `{PREFIX}habit add {name}`")
        return

    conn.execute(
        "INSERT OR IGNORE INTO habit_checks (chat_id, name, check_date) VALUES (?, ?, ?)",
        (event.chat_id, name, today),
    )
    conn.commit()
    conn.close()
    await event.edit(f"🔥 **{name}** ditandai selesai hari ini!")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}habit list$"))
async def habit_list_handler(event):
    conn = sqlite3.connect(DB_PATH)
    habits = conn.execute("SELECT name FROM habits WHERE chat_id = ?", (event.chat_id,)).fetchall()

    if not habits:
        conn.close()
        await event.edit("📭 Belum ada habit yang ditrack.")
        return

    lines = []
    for (name,) in habits:
        count = conn.execute(
            "SELECT COUNT(*) FROM habit_checks WHERE chat_id = ? AND name = ?",
            (event.chat_id, name),
        ).fetchone()[0]
        lines.append(f"- {name}: {count}x check-in")

    conn.close()
    await event.edit("📋 **Habit tracker:**\n" + "\n".join(lines))
