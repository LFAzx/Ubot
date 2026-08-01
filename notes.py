import sqlite3
from telethon import events

from client import client, PREFIX, register

DB_PATH = "notes.db"


def _init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS notes (tag TEXT PRIMARY KEY, content TEXT)")
    conn.commit()
    conn.close()


_init_db()

register(f"{PREFIX}save <tag> <teks>", "Simpan catatan (reply juga bisa)", "Notes")
register(f"{PREFIX}get <tag>", "Ambil catatan berdasarkan tag", "Notes")
register(f"{PREFIX}list", "Lihat semua tag catatan", "Notes")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}save (\S+)(?:\s([\s\S]*))?$"))
async def save_handler(event):
    tag = event.pattern_match.group(1)
    content = event.pattern_match.group(2)

    if not content and event.is_reply:
        reply = await event.get_reply_message()
        content = reply.raw_text or ""

    if not content:
        await event.edit(f"⚠️ Kasih teks atau reply pesan. Contoh: `{PREFIX}save resep nasi goreng`")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT OR REPLACE INTO notes (tag, content) VALUES (?, ?)", (tag, content))
    conn.commit()
    conn.close()
    await event.edit(f"💾 Tersimpan dengan tag `{tag}`")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}get (\S+)$"))
async def get_handler(event):
    tag = event.pattern_match.group(1)
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute("SELECT content FROM notes WHERE tag = ?", (tag,)).fetchone()
    conn.close()
    if not row:
        await event.edit(f"❌ Gak ada catatan dengan tag `{tag}`")
        return
    await event.edit(f"📌 **{tag}**\n\n{row[0]}")


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}list$"))
async def list_handler(event):
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT tag FROM notes ORDER BY tag").fetchall()
    conn.close()
    if not rows:
        await event.edit("📭 Belum ada catatan tersimpan.")
        return
    tags = ", ".join(f"`{r[0]}`" for r in rows)
    await event.edit(f"📋 **Tag tersimpan:**\n{tags}")
