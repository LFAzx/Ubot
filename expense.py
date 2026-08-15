import sqlite3
from telethon import events

from client import client, PREFIX, register

DB_PATH = "expenses.db"


def _init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        amount REAL,
        category TEXT
    )""")
    conn.commit()
    conn.close()


_init_db()

register(f"{PREFIX}expense add <jumlah> <kategori>", "Catat pengeluaran", "Produktivitas")
register(f"{PREFIX}expense list", "Lihat pengeluaran terbaru", "Produktivitas")
register(f"{PREFIX}expense total", "Total semua pengeluaran", "Produktivitas")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}expense add ([\d.]+) (.+)$"))
async def expense_add_handler(event):
    amount = float(event.pattern_match.group(1))
    category = event.pattern_match.group(2)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO expenses (chat_id, amount, category) VALUES (?, ?, ?)", (event.chat_id, amount, category))
    conn.commit()
    conn.close()
    await event.edit(f"💸 Dicatat: {amount:,.0f} untuk {category}")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}expense list$"))
async def expense_list_handler(event):
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT amount, category FROM expenses WHERE chat_id = ? ORDER BY id DESC LIMIT 20",
        (event.chat_id,),
    ).fetchall()
    conn.close()

    if not rows:
        await event.edit("📭 Belum ada pengeluaran tercatat.")
        return

    lines = [f"- {amount:,.0f} ({category})" for amount, category in rows]
    await event.edit("📋 **Pengeluaran terbaru:**\n" + "\n".join(lines))


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}expense total$"))
async def expense_total_handler(event):
    conn = sqlite3.connect(DB_PATH)
    total = conn.execute("SELECT SUM(amount) FROM expenses WHERE chat_id = ?", (event.chat_id,)).fetchone()[0] or 0
    conn.close()
    await event.edit(f"💰 **Total pengeluaran: {total:,.0f}**")
