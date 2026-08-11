import sqlite3
from telethon import events

from client import client, PREFIX, register

DB_PATH = "todo.db"


def _init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        task TEXT,
        done INTEGER DEFAULT 0
    )""")
    conn.commit()
    conn.close()


_init_db()

register(f"{PREFIX}todo add <teks>", "Tambah item to-do", "Produktivitas")
register(f"{PREFIX}todo list", "Lihat semua to-do", "Produktivitas")
register(f"{PREFIX}todo done <nomor>", "Tandai to-do selesai", "Produktivitas")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}todo add (.+)$"))
async def todo_add_handler(event):
    task = event.pattern_match.group(1)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO todos (chat_id, task) VALUES (?, ?)", (event.chat_id, task))
    conn.commit()
    conn.close()
    await event.edit(f"✅ Ditambahin: {task}")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}todo list$"))
async def todo_list_handler(event):
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT id, task, done FROM todos WHERE chat_id = ? ORDER BY id", (event.chat_id,)).fetchall()
    conn.close()

    if not rows:
        await event.edit("📭 Belum ada to-do.")
        return

    lines = []
    for id_, task, done in rows:
        mark = "✅" if done else "⬜"
        lines.append(f"{mark} {id_}. {task}")

    await event.edit("📋 **To-do list:**\n" + "\n".join(lines))


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}todo done (\d+)$"))
async def todo_done_handler(event):
    todo_id = int(event.pattern_match.group(1))
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE todos SET done = 1 WHERE id = ? AND chat_id = ?", (todo_id, event.chat_id))
    conn.commit()
    conn.close()
    await event.edit(f"✅ To-do #{todo_id} ditandai selesai.")
