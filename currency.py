import asyncio
import requests
from telethon import events

from client import client, PREFIX, register

register(f"{PREFIX}currency <jumlah> <dari> <ke>", "Convert mata uang", "Utility")


def _convert_currency(amount, from_cur, to_cur):
    resp = requests.get(f"https://open.er-api.com/v6/latest/{from_cur}", timeout=15)
    resp.raise_for_status()
    data = resp.json()

    if data.get("result") != "success":
        raise Exception("Gagal ambil data rate. Cek kode currency-nya.")

    rates = data.get("rates", {})
    if to_cur not in rates:
        raise Exception(f"Kode currency `{to_cur}` gak ditemukan.")

    result = amount * rates[to_cur]
    return result


@client.on(events.NewMessage(outgoing=True, pattern=rf"^\{PREFIX}currency ([\d.]+) (\w+) (\w+)$"))
async def currency_handler(event):
    amount = float(event.pattern_match.group(1))
    from_cur = event.pattern_match.group(2).upper()
    to_cur = event.pattern_match.group(3).upper()

    await event.edit("💱 Cek rate...")
    try:
        result = await asyncio.to_thread(_convert_currency, amount, from_cur, to_cur)
        await event.edit(f"💱 {amount:,.2f} {from_cur} = **{result:,.2f} {to_cur}**")
    except Exception as e:
        await event.edit(f"❌ Error: {e}")
