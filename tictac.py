from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}tictac start", "Mulai Tic-Tac-Toe (reply lawan main)", "Fun")
register(f"{PREFIX}tictac <1-9>", "Taruh mark di posisi 1-9", "Fun")

_games = {}

WIN_COMBOS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]


def _render(board):
    def cell(i):
        return board[i] if board[i] else str(i + 1)
    return (
        f" {cell(0)} | {cell(1)} | {cell(2)} \n"
        "---+---+---\n"
        f" {cell(3)} | {cell(4)} | {cell(5)} \n"
        "---+---+---\n"
        f" {cell(6)} | {cell(7)} | {cell(8)} "
    )


def _check_winner(board):
    for a, b, c in WIN_COMBOS:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if all(board):
        return "draw"
    return None


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}tictac start$"))
async def tictac_start_handler(event):
    if not event.is_reply:
        await event.edit("⚠️ Reply ke pesan lawan main buat mulai game.")
        return

    reply = await event.get_reply_message()
    opponent = await reply.get_sender()
    me = await event.get_sender()

    chat_id = event.chat_id
    _games[chat_id] = {
        "board": [None] * 9,
        "players": {"X": me.id, "O": opponent.id},
        "names": {"X": me.first_name, "O": opponent.first_name},
        "turn": "X",
    }

    game = _games[chat_id]
    await event.edit(
        f"⭕❌ **Tic-Tac-Toe dimulai!**\n"
        f"❌ = {me.first_name} | ⭕ = {opponent.first_name}\n\n"
        f"{_render(game['board'])}\n\n"
        f"Giliran: ❌ {me.first_name} — pakai `{PREFIX}tictac <1-9>`"
    )


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}tictac (\d)$"))
async def tictac_move_handler(event):
    chat_id = event.chat_id
    game = _games.get(chat_id)
    if not game:
        await event.edit(f"⚠️ Belum ada game aktif. Mulai dengan `{PREFIX}tictac start` (reply lawan).")
        return

    pos = int(event.pattern_match.group(1)) - 1
    if pos < 0 or pos > 8:
        await event.edit("⚠️ Posisi harus 1-9.")
        return

    sender = await event.get_sender()
    turn = game["turn"]
    expected_player = game["players"][turn]

    if sender.id != expected_player:
        await event.edit("⚠️ Bukan giliran kamu.")
        return

    if game["board"][pos]:
        await event.edit("⚠️ Posisi udah keisi, pilih yang lain.")
        return

    game["board"][pos] = "❌" if turn == "X" else "⭕"

    result = _check_winner(game["board"])
    if result == "draw":
        await event.edit(f"🤝 **Seri!**\n\n{_render(game['board'])}")
        del _games[chat_id]
        return
    elif result:
        winner_symbol = "X" if result == "❌" else "O"
        winner_name = game["names"][winner_symbol]
        await event.edit(f"🎉 **{result} ({winner_name}) menang!**\n\n{_render(game['board'])}")
        del _games[chat_id]
        return

    game["turn"] = "O" if turn == "X" else "X"
    next_symbol = "❌" if game["turn"] == "X" else "⭕"
    next_name = game["names"][game["turn"]]
    await event.edit(
        f"{_render(game['board'])}\n\n"
        f"Giliran: {next_symbol} {next_name} — pakai `{PREFIX}tictac <1-9>`"
    )
